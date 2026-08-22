# Safe Mutation Workflow

Use this reference when a Unity task touches serialized scenes, prefabs, generated
programs, a dirty checkout, a persistent Apply tool, or an action that may outlive
the MCP request.

## Take over without destroying context

1. Read the repository instructions that govern the target.
2. Inspect branch, HEAD/tag, stash state, and the scoped tracked/untracked diff.
3. Name the files and Unity objects allowed to change.
4. Preserve every unrelated change. Stage only an explicit allowlist when a commit is requested.
5. Verify current state directly when a document, result, or handoff may be stale.

Do not use cleanup as a prerequisite for implementation. A dirty checkout is a
scope-control problem, not permission to reset, stash, clean, or overwrite it.

## Prove the owner and mutation path

Build the smallest complete chain relevant to the change:

```text
authoring/source owner
  -> importer, builder, or serialized binding
  -> scene/prefab/runtime owner
  -> visible or behavioral consumer
```

Prefer the current saved scene and current serialized references over legacy
builders. Treat a one-shot migration as frozen history unless its owned hierarchy
and purpose are explicitly re-authorized.

## Run a transactional scene mutation

Use this order:

```text
select exact Editor instance
  -> verify correct project and scene
  -> verify idle, saved, and outside Prefab Stage
  -> verify required compiled and UdonSharp program assets
  -> complete read-only preflight
  -> open one Undo group
  -> mutate declared targets
  -> run targeted checks
  -> save once
  -> wait for import, domain reload, and delayed writeback
  -> confirm stable clean state and new Console errors
```

Roll back the full Undo group on every failure before the final save. Do not let
an Apply discover missing dependencies, start compilation, or create required
ProgramAssets halfway through its mutations.

## Recover after timeout or disconnect

A transport response is not the operation result. After timeout or disconnect:

1. Do not invoke the action again.
2. Rediscover the exact Editor instance and session.
3. Inspect the existing run identity and durable result.
4. Inspect intended outputs, scene dirtiness, compilation state, and new Console errors.
5. Classify the run from those facts: completed, still running, failed, or blocked.

Retry only after proving that the prior run is terminal and that repeating it is
safe. Stop after the same automation method fails twice.

## Close out proportionately

For routine work, report the changed scope, compile/import outcome, targeted
evidence, and any blocker that affects the requested claim. Do not manufacture a
full acceptance matrix or enumerate unrelated runtime layers.
