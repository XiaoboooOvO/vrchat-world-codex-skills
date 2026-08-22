#!/usr/bin/env python3
"""Read-only, deterministic audit for a VRChat Worlds project."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
EXCLUDED_DIRS = {"Library", "Temp", "Logs"}


def normalize_relative(path: str | Path) -> str:
    return Path(path).as_posix().lstrip("./")


def is_excluded(relative_path: str | Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in Path(relative_path).parts)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def utc_mtime(path: Path) -> str:
    return (
        datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def file_record(project: Path, relative_path: str | Path) -> dict[str, Any]:
    relative = normalize_relative(relative_path)
    record: dict[str, Any] = {"path": relative, "excluded": is_excluded(relative)}
    if record["excluded"]:
        record.update({"exists": False, "reason": "excluded_directory"})
        return record

    path = project / Path(relative)
    record["exists"] = path.is_file()
    if not record["exists"]:
        return record

    stat = path.stat()
    record.update(
        {
            "bytes": stat.st_size,
            "mtimeUTC": utc_mtime(path),
            "sha256": sha256_file(path),
        }
    )
    return record


def parse_project_version(project: Path) -> dict[str, Any]:
    relative = "ProjectSettings/ProjectVersion.txt"
    result: dict[str, Any] = {"file": file_record(project, relative)}
    path = project / relative
    if not path.is_file():
        return result

    text = read_text(path)
    for key in ("m_EditorVersion", "m_EditorVersionWithRevision"):
        match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
        if match:
            result[key] = match.group(1).strip()
    return result


def load_json(path: Path, relative: str, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(read_text(path))
    except OSError as exc:
        errors.append(f"{relative}: {type(exc).__name__}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"{relative}: invalid JSON at line {exc.lineno}, column {exc.colno}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{relative}: top-level JSON must be an object")
        return None
    return value


def package_versions(project: Path, errors: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for relative in ("Packages/manifest.json", "Packages/vpm-manifest.json"):
        package_file: dict[str, Any] = {"file": file_record(project, relative)}
        data = load_json(project / relative, relative, errors)
        dependencies = data.get("dependencies") if data else None
        if isinstance(dependencies, dict):
            versions: dict[str, str] = {}
            for name, value in sorted(dependencies.items()):
                package_name = str(name)
                if not package_name.startswith("com.vrchat."):
                    continue
                if isinstance(value, str):
                    versions[package_name] = value
                elif isinstance(value, dict) and isinstance(value.get("version"), str):
                    versions[package_name] = value["version"]
                else:
                    errors.append(
                        f"{relative}: {package_name} has unsupported dependency shape"
                    )
            package_file["vrchatPackages"] = versions
        result[relative] = package_file
    return result


def parse_build_settings(project: Path) -> dict[str, Any]:
    relative = "ProjectSettings/EditorBuildSettings.asset"
    result: dict[str, Any] = {"file": file_record(project, relative), "scenes": []}
    path = project / relative
    if not path.is_file():
        return result

    current: dict[str, Any] | None = None
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if line.startswith("- enabled:"):
            if current is not None:
                result["scenes"].append(current)
            current = {"enabled": line.split(":", 1)[1].strip() == "1"}
        elif current is not None and line.startswith("path:"):
            current["path"] = line.split(":", 1)[1].strip()
        elif current is not None and line.startswith("guid:"):
            current["guid"] = line.split(":", 1)[1].strip()
    if current is not None:
        result["scenes"].append(current)
    result["scenes"] = sorted(
        result["scenes"], key=lambda scene: (str(scene.get("path", "")), bool(scene.get("enabled")))
    )
    result["scenePaths"] = [
        scene["path"] for scene in result["scenes"] if isinstance(scene.get("path"), str)
    ]
    return result


def git_validity(project: Path) -> dict[str, Any]:
    command = ["git", "-C", str(project), "rev-parse", "--is-inside-work-tree"]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"valid": False, "error": type(exc).__name__}

    output = completed.stdout.strip()
    return {
        "valid": completed.returncode == 0 and output == "true",
        "returncode": completed.returncode,
        "output": output,
    }


def unique_paths(paths: Iterable[str]) -> list[str]:
    return sorted({normalize_relative(path) for path in paths})


def build_audit(project: Path) -> dict[str, Any]:
    errors: list[str] = []
    build_settings = parse_build_settings(project)
    vrchat_packages = package_versions(project, errors)
    scene_paths = [
        path for path in build_settings.get("scenePaths", []) if isinstance(path, str)
    ]
    core_paths = unique_paths(
        [
            "AGENTS.md",
            "ProjectSettings/ProjectVersion.txt",
            "ProjectSettings/EditorBuildSettings.asset",
            "Packages/manifest.json",
            "Packages/vpm-manifest.json",
            *scene_paths,
        ]
    )
    scene_existence = [
        {"path": path, "exists": (project / Path(path)).is_file()}
        for path in scene_paths
        if not is_excluded(path)
    ]
    return {
        "status": "FAIL" if errors else "PASS",
        "errors": sorted(errors),
        "schemaVersion": SCHEMA_VERSION,
        "project": str(project),
        "projectVersion": parse_project_version(project),
        "vrchatPackages": vrchat_packages,
        "buildSettings": build_settings,
        "agentsAndScenes": {
            "agents": file_record(project, "AGENTS.md"),
            "majorScenes": sorted(scene_existence, key=lambda item: item["path"]),
        },
        "git": git_validity(project),
        "coreFiles": [file_record(project, path) for path in core_paths],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="VRChat project directory")
    parser.add_argument(
        "--output",
        required=False,
        type=Path,
        help="JSON output path; omit it to write only to stdout",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        print(f"project directory does not exist: {project}", file=sys.stderr)
        return 2

    payload = json.dumps(
        build_audit(project), ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    if args.output is not None and str(args.output) != "-":
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8", newline="\n")
    sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
