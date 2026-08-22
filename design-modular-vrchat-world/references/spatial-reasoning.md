# Spatial Reasoning

Use this reference before assigning exact transforms or judging whether a module
layout works.

## Keep coordinate spaces explicit

Name the space for every measurement:

- world space for assembling modules;
- module-local space for internal structure and anchors;
- surface-local space for content mounted on walls, boards, or tables;
- camera, viewport, screen, or Canvas space for rendered UI.

Do not combine coordinates from different spaces without an explicit conversion.
Place and rotate a module root in world space; design its children in local space.

## Reason from constraints before coordinates

For each module, check:

- bounds, floor level, ceiling, and required clearance;
- entry position, facing, and first visible landmark;
- exit and recovery or return path;
- walkable route and congestion points;
- interaction reach, viewing distance, and surface normal;
- primary and secondary sightlines;
- spectator and operator separation when roles differ;
- sound, light, mirror, camera, and screen spill across module boundaries;
- whether the whole module can move or rotate without breaking internal logic.

Use approximate dimensions during planning. Choose exact values only after the
project scale, avatar assumptions, existing anchors, and asset bounds are known.

## Use spatial interfaces

Define ports instead of loosely saying two rooms connect. A port includes a type,
position, facing, clearance, and compatibility condition. Define placement
surfaces with center, normal, usable bounds, and content type.

Treat cameras, spectator views, audio openings, and state-only dependencies as
interfaces even when players cannot traverse them.

## Avoid common failures

- Do not place objects from prose one by one before establishing module bounds.
- Do not use world coordinates for every child.
- Do not move a visible panel without its decoration, colliders, interaction, and anchors.
- Do not scale child UI to compensate for an oversized or rotated parent without inspecting the full transform chain.
- Do not arrange spaces only from a top-down footprint; include height, facing, visibility, and reach.
- Do not make every connection a teleport when continuous orientation matters.
- Do not let a camera or screen capture itself unless recursive presentation is intentional.
