# Module Model

Use this model to turn a spatial idea into a small number of understandable
places before creating Unity objects. Use only the fields needed by the task.

## Player journey

Write a short action chain for each relevant role:

```text
arrive -> orient -> choose -> act -> receive feedback -> continue or return
```

Mark decisions, one-way transitions, recovery paths, and places where roles
diverge. A list of rooms without player actions is not a journey.

## Module graph

Represent modules as nodes and connections as typed edges:

- `walk`: continuous physical path;
- `door`: bounded opening with a direction or access condition;
- `teleport`: discontinuous spatial transfer;
- `view`: visible but not traversable relationship;
- `state`: informational or runtime dependency without spatial adjacency.

Do not assume adjacent modules must share a parent or that dependent systems must
share a physical space.

## Module card

```yaml
module:
  id: gameplay-zone
  purpose: Primary gameplay area
  users: [player, spectator]

  frame:
    origin: [0, 0, 0]
    forward: [0, 0, 1]
    up: [0, 1, 0]

  bounds:
    size: [12, 6, 18]

  ports:
    - id: player-entry
      type: walkway
      position: [0, 0, -9]
      facing: [0, 0, 1]

  placement_surfaces:
    - id: status-display
      type: world-ui
      center: [0, 2, 8.5]
      normal: [0, 0, -1]
      size: [5, 2]

  owned_content: [structure, interaction, presentation]
  dependencies: [match-state-reader]
  must_move_together: [structure, colliders, interaction, anchors, presentation]
```

Treat this as a reasoning form, not a schema that every project must store.

## Split or merge test

Split a module when it has multiple unrelated primary purposes, incompatible user
permissions, conflicting traffic or sightline requirements, or different roots
that must move independently.

Merge nearby elements when they share one purpose, move as a unit, use the same
local frame, and would be harder to maintain across separate owners.

Keep global systems outside spatial modules only when their lifetime and
responsibility genuinely cross module boundaries.
