# Unity MCP Workflow

Use Unity MCP only as an explicit, bounded bridge to a Unity Editor that the user has already started. Resolve the workflow in this order:

```text
custom-tools -> instances -> editor state -> menu items
```

The user's scoped approval in chat is an explicit start. Codex may perform safe intermediate checks, monitor compilation, and invoke one exact authorized menu item without requiring the user to switch to Unity and click it manually. Do not extend that approval to Play Mode, ClientSim, rebuilds, Build & Test, uploads, or another side effect.

## 1. Discover custom tools

Confirm which MCP tools are actually available before using them. A tool name in a prompt is not proof that the current connection exposes it. Do not substitute an unrelated tool or silently widen permissions.

## 2. Select an explicit instance

Enumerate the connected Unity instances and select one explicit instance identifier. Check that it is the expected project and editor session. Never guess an instance, broadcast a menu action, or operate on multiple instances in parallel.

## 3. Check editor state

Before any action, confirm the selected instance is the intended project, is not compiling or updating, and is not in Play Mode unless the explicit workflow owns that Play Mode. If the same project is already open in the Unity Editor, do not start Unity batch mode. Do not close, restart, or take ownership of another editor without explicit user consent.

## 4. Compile without user switching

For source changes, finish the bounded edit batch, trigger import/compilation once through the available Unity script workflow, and poll editor state until compilation and domain reload complete. Read new Console errors from a cursor or sequence baseline. Do not ask the user to focus Unity merely to start or wait for compilation, and do not refresh after every edited file.

## 5. Execute one explicit menu item

Use the narrowest permission set needed. Read-only inspection normally needs only `read_console`, `find_gameobjects`, and `unity_reflect`. Temporarily add `execute_menu_item` only when the user explicitly authorizes one known menu action; do not add broad execution, file, or process permissions. Invoke the exact menu item once, with a bounded timeout, and wait for its persistent project-owned result. Do not auto-build scenes, save assets, start ClientSim, or chain another menu item.

For a lightweight scene patch, the menu item itself starts with the read-only safety gate and writes one compact result. A separate Preflight menu, contract, or full baseline is not required by default. For a high-risk lifecycle/build action, require the full project contract, authorization, timeout, and persistent result before invocation.

## Risk-scaled evidence and transport

- Fast source change: compilation and targeted Console/static evidence are sufficient; no result artifact is required by default.
- Lightweight scene patch: prefer its compact project-owned result over the transient MCP response.
- High-risk lifecycle/build: require the current contract, authorization identity, persistent result, and transport record.

If an authorized menu action writes a durable, current result with `overallStatus: PASS` and the connection then drops, preserve the artifact `PASS` and mark transport as `DEGRADED`; do not retry the menu action. A missing, stale, or incomplete required result is not a gameplay failure: classify the run as `BLOCKED`.

Record only what the risk tier requires. Keep contract/hash identity for high-risk runs, not routine source edits. Always read Console incrementally and do not treat old Console text as evidence for the current action.
