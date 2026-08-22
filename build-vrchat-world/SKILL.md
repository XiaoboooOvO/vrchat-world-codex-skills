---
name: build-vrchat-world
description: Safely inspect, implement, diagnose, and repair Unity VRChat Worlds projects with bounded source edits, serialized scene or prefab work, Unity MCP operations, UdonSharp workflows, generated content pipelines, and explicitly requested runtime or build actions.
---

# Build VRChat World

Use this skill for execution safety. For a new world, room, zone, player journey,
spatial layout, graybox, or semantic hierarchy, use
`design-modular-vrchat-world` first and return here only after the module boundary
is clear.

Choose exactly one primary mode and use the lowest-risk mode that satisfies the request:

- **Offline docs/authoring** - edit project documentation or authoring data that Unity does not need to import; skip Unity, MCP, compilation, scene checks, and result artifacts.
- **Read-only diagnose** - inspect the live project and evidence; do not write, rebuild, save, or enter Play Mode.
- **Fast source change** - edit bounded source files, let Unity import and compile once, then check new Console errors and targeted static evidence.
- **Lightweight scene patch** - invoke one explicitly authorized Apply entry point whose first step is a read-only Unity safety gate, then save once and emit one compact result.
- **Explicit runtime/build** - run Play Mode, ClientSim, Build & Test, or upload only when the user asks for that operation.

Do not automatically upgrade an offline task, fast change, or lightweight patch into a high-risk workflow.

## Interaction and review budget

1. Read the project `AGENTS.md` before acting; project rules may narrow these defaults.
2. Treat a user's scoped approval in chat as the explicit start for that task. Complete safe intermediate work, Unity compilation monitoring, and one exact authorized menu invocation without asking the user to click through each step.
3. Do not infer authorization for Play Mode, ClientSim, scene rebuild, Build & Test, upload, or another materially different side effect.
4. Do not load testing documents, run acceptance work, or list unrun tests unless the user reports a problem, asks for testing, or is deciding a release.
5. For routine work, use one scoped Git summary and the smallest check needed to avoid an obviously broken change. Expand only after a failure or conflicting evidence.

## Establish live truth before editing

- Prefer current Git, project files, serialized references, and the selected Editor session over document headers, old tags, handoff notes, screenshots, or prior PASS artifacts.
- Inspect the scoped dirty state before writing. Preserve unrelated tracked and untracked work; do not reset, clean, stash, overwrite, or broadly stage it.
- Identify the current source of truth, the runtime or serialized owner, and the supported mutation path. Treat old builders and one-shot Apply tools as frozen migrations unless the project explicitly authorizes reuse.
- Trace generated content in one direction: authoring source -> validator/importer -> generated assets -> serialized references -> runtime consumer. Do not reverse-write a generated artifact into its authoring source without an explicit project contract.
- If ownership remains ambiguous and choosing one path would change behavior or broaden scope, stop and ask one focused question.

## Risk-scaled workflow

### Offline docs/authoring

- Read only the directly relevant project rule, contract, and scoped files. Do not enumerate historical Apply tools or scan all artifacts and logs unless the issue points there.
- Validate content and format locally. Do not connect to Unity or MCP, compile, create result JSON, or run full static acceptance.
- Prefer compact counts, statuses, diffs, and scoped excerpts over recursive listings, full logs, or full data dumps.

### Fast source change

- Preserve unrelated work and edit only the approved files.
- Do not create a contract, full baseline manifest, result JSON, or dedicated Preflight menu unless project rules or the user require one.
- Finish a related edit batch before triggering Unity import/compilation once. Poll editor state until compilation and domain reload finish, then inspect only new errors.
- Fix bounded compile errors when safe; stop after the same method fails twice.

### Lightweight scene patch

- Use one explicit Apply entry point. Chat approval may authorize Codex to invoke that exact entry point through Unity MCP; the user does not need to click it manually.
- Begin Apply with a shared read-only gate: correct instance and scene, not playing or transitioning, not compiling or updating, no Prefab Stage, and no unsaved target-scene changes.
- After the gate passes, modify only authorized targets, save once, run targeted static checks, and write one compact result. On gate failure, exit with zero side effects.
- Do not split a routine patch into Preflight, Apply, and Static Acceptance menus by default. Keep runtime acceptance separate.
- Never hard-code a one-run timestamp, old scene SHA, contract filename, or result filename into a reusable executor.
- Prepare and verify required UdonSharp ProgramAssets before mutation. Do not compile or generate them halfway through an Apply.
- Complete a zero-side-effect preflight before opening one Undo group. Modify only declared targets, roll back the entire group on failure, and save only after all targeted checks succeed.

### Explicit runtime/build

- Use explicit menu or automation entry points. Never start runtime or build work on editor load, script reload, or scene open.
- Give Play Mode to one owner at a time. Do not run batch mode while the same project is open in Unity, and do not close that editor without consent.
- Set a timeout and clean up owned Play Mode or callbacks on every terminal path. Stop after the same automation method fails twice.
- Read [references/unity-lifecycle-and-acceptance.md](references/unity-lifecycle-and-acceptance.md) only for an explicitly requested runtime, acceptance, build, or upload task.

## Completion and retry rules

- Treat request return, timeout, transport loss, `STARTED`, and `PENDING` as non-terminal states. Inspect the same run's durable result, generated output, scene state, and new Console messages before deciding whether it succeeded or failed.
- Never repeat a possibly mutating action while the same run may still be active. Reconnect and inspect first.
- Bind any durable PASS to the current source or input identity, target scene, Editor session when relevant, changed targets, and stable post-save state. Do not reuse a historical PASS as current proof.
- After the same automation method fails twice, preserve the failure evidence, report the blocker, and change the diagnosis or ownership model instead of guessing another path.
- Report only the evidence needed for the requested task. Do not automatically list ClientSim, desktop, VR, multiplayer, build, or upload as `NOT_RUN`; mention an unexecuted layer only when the user asked about it or the claim would otherwise be misleading.

## World implementation guardrails

Keep local gameplay state local unless synchronization is explicitly requested. Every state-changing event receiving `VRCPlayerApi player` must begin with:

```csharp
if (player == null || !player.isLocal) return;
```

When editor code creates UdonSharp behaviours, use:

```csharp
gameObject.AddUdonSharpComponent<MyBehaviour>();
```

Do not substitute plain `AddComponent<T>()` for UdonSharp components. Route jump settings, checkpoints, kill triggers, respawn height, and other world-mechanics patterns to [references/vrchat-world-implementation.md](references/vrchat-world-implementation.md).

Read [references/safe-mutation-workflow.md](references/safe-mutation-workflow.md)
for dirty-worktree takeover, source-of-truth tracing, transactional Apply, or
timeout/reconnect recovery. Read
[references/generated-content-workflow.md](references/generated-content-workflow.md)
for authoring/import/generation/Bake pipelines or generated TMP glyph atlases.

For Unity MCP instance selection and unattended compilation details, read
[references/unity-mcp-workflow.md](references/unity-mcp-workflow.md) only when
Unity MCP is actually used.
