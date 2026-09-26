---
name: design-modular-vrchat-world
description: Define or revise functional module boundaries, ownership, and interfaces in Unity or VRChat worlds. Use when spatial decomposition is needed; skip routine local edits inside known boundaries and coordinate conversions.
---

# Design Modular VRChat World

Use this skill only when a task needs module boundaries, responsibilities, or interfaces defined or revised. For local work inside known boundaries, use build-vrchat-world directly. For coordinate-frame or import-angle analysis, use coordinate-transform-audit; that skill does not require modularization.

Design those boundaries before implementation; do not jump from a natural-language request directly to GameObjects or world coordinates.

After the design is clear, use build-vrchat-world only when implementation is in scope. This skill alone does not authorize Unity mutation.

## Choose the output depth

Use **Quick mode** when one small module needs a concise boundary or interface design. Produce only:

- purpose and users;
- local frame and approximate bounds;
- entry, exit, primary sightline, and interaction surface;
- semantic hierarchy and implementation order.

Use **Full mode** for a new world, three or more connected modules, broad spatial
reorganization, or an unclear player journey. Produce:

- player journey;
- module graph;
- module cards;
- ports, sightlines, placement surfaces, and constraints;
- semantic Unity hierarchy;
- graybox and per-module implementation order;
- cross-module interfaces and open decisions.

Do not create a persistent design document unless the user asks for one. When
they do, copy and adapt [assets/module-plan-template.md](assets/module-plan-template.md).

## Follow the design sequence

### 1. Model the player journey

Describe what each user role does from arrival to exit. Use actions and decisions,
not object lists. Include recovery or return paths when they matter.

### 2. Create the module graph

Turn each distinct spatial responsibility into a module. Represent adjacency,
visibility, physical travel, teleport, and state-only connections explicitly.

A module should normally have one primary purpose. Split it when unrelated user
roles, conflicting interaction rules, or different spatial conditions make it
hard to explain as one place.

### 3. Define module interfaces

For each module, define its local frame, approximate bounds, ports, sightlines,
interaction zones, placement surfaces, owned content, runtime owner, dependencies,
and elements that must move together. Read
[references/module-model.md](references/module-model.md) for the compact model.

### 4. Design the semantic hierarchy

Group objects by spatial and functional ownership, not only by component type.
Keep structure, colliders, interaction, presentation, runtime bindings, and
anchors under the module they serve. Put only genuinely cross-module systems at
the world level. Read
[references/semantic-hierarchy.md](references/semantic-hierarchy.md) when creating
or reorganizing a hierarchy.

### 5. Establish spatial constraints

Keep world, module-local, surface-local, camera, and Canvas spaces explicit.
Reason from bounds, forward direction, entries, exits, reach, clearance, and
sightlines before choosing coordinates. Read
[references/spatial-reasoning.md](references/spatial-reasoning.md) for spatial
checks and anti-patterns.

### 6. Plan implementation by module

First assemble the complete world as low-detail modules. Then complete one module
through structure, interaction, runtime ownership, and presentation before
repeating the proven pattern elsewhere. Integrate cross-module connections last.

Prefer this sequence:

```text
world module graph
  -> module frames, bounds, and ports
  -> whole-world graybox
  -> one functional module slice
  -> repeated module slices
  -> cross-module integration
  -> presentation and polish
```

## Preserve existing projects

- Derive existing module names, owners, scene roots, prefabs, and coordinate frames from the live project.
- Treat the suggested hierarchy as a fallback, not a mandatory migration target.
- Preserve stable serialized references and established owners.
- Do not reorganize merely for visual neatness; require a clearer ownership, movement, or maintenance boundary.
- Move a semantic unit with its colliders, UI, interaction, anchors, and runtime bindings while preserving world transforms unless the design intentionally changes placement.

## Hand off to implementation

End an implementation-ready design with:

```text
Module in scope:
Existing owner or proposed root:
Local frame and bounds:
Ports and placement surfaces:
Objects that move together:
Cross-module interfaces:
Do-not-touch boundaries:
Graybox completion condition:
Open decisions:
```

Do not choose exact Unity mutation tools, run Apply, or enter runtime modes here.
Pass this boundary to `build-vrchat-world`.
