# Unity Lifecycle and Acceptance

Use this reference for explicit Unity lifecycle control and layered VRChat world acceptance. It applies to builders, acceptance runners, ClientSim, and Build & Test helpers.

## State and ownership

- `SessionState` is for one editor session only. Do not use `EditorPrefs` for project workflow state.
- State that must survive a domain reload or process restart belongs in a project-owned, inspectable file under the relevant artifact directory.
- A project may have only one Play Mode owner at a time. A builder, acceptance runner, ClientSim session, or Build & Test helper must not start, stop, or preempt another owner's Play Mode.
- Scene build, asset save, ClientSim, acceptance, and Build & Test are explicit menu or automation actions. Do not start them from editor load, script reload, scene open, or other static initialization.
- If the same project is open in Unity Editor, do not run Unity batch mode. Do not close that editor without explicit user consent.

## Risk-scaled contracts and evidence

- A fast source change needs scoped authorization, preserved unrelated work, one compilation cycle, and targeted evidence; it does not need a standalone contract or result artifact by default.
- A lightweight scene patch needs an internal read-only safety gate, one authorized Apply invocation, one save, and one compact result; it does not need a full baseline or one-shot authorization by default.
- A high-risk lifecycle/build run needs a machine-readable contract containing the scope, start time, Unity version, scene path, relevant source/scene/settings hashes, intended entry point, and authorization identity. Acceptance must reject a high-risk run when its source, scene, settings, run identity, or timestamps are stale.

Persistent high-risk evidence belongs in project-owned paths such as:

- `Artifacts/<WorldOrFeature>/Build/` for build records and traces.
- `Artifacts/<WorldOrFeature>/Acceptance/` for acceptance state, summaries, and results.

`Temp/`, Console text, and `ClientSimStorage/` may be diagnostic inputs but must not be the only acceptance evidence. A high-risk result without a current contract, current hashes, or a valid completion record is stale and cannot be reported as a pass.

## Explicit lifecycle and cleanup

Every flow that waits across frames or reloads, owns Play Mode, or performs a high-risk build must set a total timeout before starting. On success, failure, or timeout it must remove callbacks, restore temporary scene/editor state, exit only the Play Mode it started, close or clear its active state, and leave a persistent result explaining the outcome. A timeout or missing result is a tool/environment blocker, not proof that gameplay failed.

## Incremental Console evidence

Read Console output incrementally using a cursor, sequence number, or byte/line offset captured at the start of the run. Record only new messages for the current run and keep the cursor with the result. Do not treat old Console output as evidence for a new run; clear or re-baseline the cursor when the editor session changes.

## Acceptance summary

Machine-readable automated acceptance output should include the following fields:

```json
{
  "gameplayStatus": "NOT_RUN",
  "consoleStatus": "NOT_RUN",
  "artifactStatus": "NOT_RUN",
  "transportStatus": "NOT_RUN",
  "manualStatus": "NOT_RUN",
  "overallStatus": "NOT_RUN"
}
```

Overall and gameplay-related statuses use only `PASS`, `PASS_WITH_ISSUES`, `FAIL`, `BLOCKED`, or `NOT_RUN`. `transportStatus` may additionally be `DEGRADED`, but only when a persistent result is already trusted and the subsequent transport connection breaks. `overallStatus` must not claim a stronger layer than the evidence supports. Keep static audit, Unity import/C# compile, UdonSharp compile, ClientSim gameplay, desktop interaction, VR hardware, and two-client Build & Test as separate checks.

## BLOCKED versus FAIL

- `FAIL` means the requested check ran against current evidence and the product or gameplay assertion failed.
- `BLOCKED` means the check could not run or its evidence could not be trusted because of licensing, IPC/transport, timeout, missing result, stale evidence, wrong Unity ownership, or another environment/tool condition.
- A transport failure after a durable result is written does not erase that result: keep the artifact status, mark transport as degraded or blocked as appropriate, and do not retry the same automation method more than twice.
