"""Exit-status tests for build-vrchat-world/scripts/audit_vrchat_world.py (no Unity needed)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "build-vrchat-world" / "scripts" / "audit_vrchat_world.py"


def run_audit(project: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project", str(project)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class AuditExitStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def make_project(self, name: str, manifest: str) -> Path:
        project = self.root / name
        (project / "Packages").mkdir(parents=True)
        (project / "Packages" / "manifest.json").write_text(manifest, encoding="utf-8")
        return project

    def test_clean_project_exits_zero(self) -> None:
        result = run_audit(self.make_project("ok", '{"dependencies": {}}'))
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")
        self.assertEqual(result.returncode, 0)

    def test_broken_manifest_fails_with_exit_one(self) -> None:
        project = self.make_project("bad", "{not json")
        before = (project / "Packages" / "manifest.json").read_bytes()
        result = run_audit(project)
        self.assertEqual(json.loads(result.stdout)["status"], "FAIL")
        self.assertEqual(result.returncode, 1)
        self.assertEqual((project / "Packages" / "manifest.json").read_bytes(), before)

    def test_missing_project_exits_two(self) -> None:
        result = run_audit(self.root / "missing")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
