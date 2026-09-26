# VRChat World Feature Contracts

Read this reference only when the World implements one of these feature families:
World-to-external event transport, Udon multiplayer, synchronized mechanisms or
animation, or UdonSharp program serialization. Keep exact URLs, event IDs,
object names, player-slot policy, and state names in the project's own contract.

## World-to-external event bridge

Treat the World as a constrained client of an external service:

- Define which command fields the World owns and which behavior, limits, cooldown,
  or device safety remains external. Do not invent hidden parameters or reverse
  the project's declared request contract.
- Prefer serialized, project-approved URLs or endpoints. Do not construct a
  runtime URL through an SDK API that is not exposed to Udon; validate event IDs,
  URL permissions, and required serialized references before sending.
- For `VRCStringDownloader.LoadUrl`, treat the request callback as asynchronous:
  `PENDING` is non-terminal, and only the callback's success state can establish
  World-side request success. A configured URL is not network or device proof.
- On a missing reference, unsupported URL construction, invalid command, or
  blocked endpoint, remain fail-closed and expose a blocked/error state. Do not
  claim external service or device output from World-side evidence.

## Udon multiplayer

- State the authority object and the difference between synchronized state,
  network events, and local presentation before editing. Use the project's
  authority contract; do not substitute Master or Instance Owner for object
  ownership without an explicit contract.
- Use a stable player identity such as the project-defined player ID, not a
  display name, for registration and target routing. The receiving path must
  validate the actual network caller, target identity, current registration,
  event/version, and request data before applying a local effect.
- Keep the synchronized state authoritative. Serialize only at the defined
  commit point, and do not treat a sender-side state change or a local display
  update as remote success.
- When the feature depends on it, define behavior for player leave, late join,
  owner transfer, and `OnDeserialization`; otherwise keep those cases explicitly
  outside the current contract.
- This section is for VRChat Udon networking. Do not route it to Unity
  Multiplayer Services APIs unless the project explicitly uses those services.

## Synchronized mechanisms and animation

- Separate the input trigger or sensor, the authoritative mechanism state, and
  the Animator or other visual presenter. The state is the source of truth; the
  animation reflects it.
- Define the supported states and transitions, including repeated input, open /
  close races, reset, and the behavior when a late or duplicate event arrives.
- Synchronize the smallest meaningful state or event needed by the mechanism;
  do not make a visual animation frame stream the authority unless the project
  explicitly requires that design.
- Check local presentation and remote presentation separately when the
  mechanism is networked. A local Animator transition alone is not multiplayer
  evidence.

## World-space UI placement

For World Space UI in a VRChat World, use a serialized viewpoint or interaction
anchor as the placement reference. Express the UI position and size in world
units relative to that anchor; do not derive placement only from the world
origin or screen-space pixel values.

Keep the following together as the layout contract:

- the anchor;
- the local position offset;
- the local rotation;
- the UI size or scale; and
- any deliberate depth separation between UI layers or surfaces.

If an approved placeholder exists, its Transform and layout values are the
source of truth. Replace the placeholder by transferring those values; do not
re-infer them while creating the final Canvas or controls. If the layout depends
on a viewpoint that has not been specified, leave that dependency unresolved
instead of silently inventing a different viewpoint.

An approach or facing direction is optional. Add one only when the UI design
depends on a known approach or visible front; do not require every world UI to
face a user or assume a universal arrival direction. When a facing direction is
used, declare the UI root's visible local front explicitly and preserve its
rotation. A reusable Prefab may adopt local `+Z` as that root convention, but
first normalize its internal Canvas/content so the rendered readable side
actually agrees with `+Z`; do not infer readability from `Transform.forward`.
Before accepting placement, inspect from the serialized interaction/viewpoint
anchor and confirm text is not mirrored. A shared world UI remains fixed unless
per-player presentation was explicitly designed.

## UdonSharp program and scene serialization chain

Keep this one-way chain intact:

```text
UdonSharp source
  -> UdonSharp ProgramAsset
  -> SerializedUdonProgram
  -> backing UdonBehaviour on the current Prefab/Scene
  -> runtime consumer
```

- Before a scene or prefab mutation, verify that the required ProgramAsset exists
  and is ready for the target source. Do not create or discover required generated
  programs halfway through a mutation.
- After a source change, wait for import, compilation, and domain reload, then
  verify the generated program, backing behaviour, serialized references, public
  event/method names, and the intended current scene or prefab.
- Repair the source or supported generation path rather than hand-editing a
  generated SerializedUdonProgram. A clean source check or Udon compile does not
  prove that the current serialized behaviour or runtime consumer is correct.

## Evidence boundary

State only what the current contract and task-relevant checks establish. Local World behavior does not prove a remote player or external service acted successfully. Mention an unresolved dependency when it affects the requested outcome.