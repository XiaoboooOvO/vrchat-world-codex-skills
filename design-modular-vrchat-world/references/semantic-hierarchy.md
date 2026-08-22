# Semantic Unity Hierarchy

Organize a scene so a human can identify, move, replace, and maintain one spatial
module without searching across unrelated component-type roots.

## Fallback hierarchy

Use this only when the live project has no stronger convention:

```text
WorldRoot
├── GlobalSystems
├── Modules
│   ├── Arrival
│   │   ├── Structure
│   │   ├── Interaction
│   │   ├── Presentation
│   │   ├── Runtime
│   │   └── Anchors
│   ├── Lobby
│   ├── Gameplay
│   └── Results
├── Connections
└── SharedEnvironment
```

Do not force these exact names. Derive the project's language and preserve stable
owners and serialized paths.

## Ownership rules

- Keep a module's structure, collision, interaction, presentation, runtime bindings, and anchors under its semantic root.
- Keep doors, corridors, teleports, and shared sightlines in the owner selected by the project; use a `Connections` root only when neither adjacent module should own them.
- Keep truly global lifecycle, networking, audio, settings, and shared services outside spatial modules.
- Keep local presenters and effects inside the module that consumes them; do not move authority merely to make the hierarchy symmetrical.
- Prefer references or narrow interfaces across modules instead of direct access to another module's internals.

## Reorganization rules

Reorganize only when it improves ownership, independent movement, replacement,
or maintenance. Before reparenting, identify everything that must move together,
serialized references that depend on the path or object, prefab relationships,
and world-transform preservation requirements.

Do not organize the scene primarily as:

```text
AllMeshes
AllCanvases
AllColliders
AllScripts
AllLights
```

Component-type folders split one human concept across the entire hierarchy.
Component grouping is acceptable inside a clear module or for a genuine global
service collection.

## Module implementation order

Within one module, prefer:

```text
purpose and bounds
  -> local frame and anchors
  -> graybox structure
  -> paths, colliders, and interaction surfaces
  -> runtime owner and bindings
  -> presentation
  -> cross-module interfaces
```

Do not polish all modules before one representative module has a complete
functional slice.
