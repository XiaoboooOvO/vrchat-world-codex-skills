# VRChat World Implementation Notes

## Technical Baseline Scene

For jump or trap worlds, make a disposable baseline scene before the real level:

- `PlayerMovementSettings` object with exposed fields for jump, walk, run, strafe, and gravity.
- Optional height enforcer only when the design requires controlled eye height for measurement.
- 3 to 5 measurement gaps from narrow to wide.
- Default respawn point facing the forward route.
- Numbered checkpoint trigger.
- Thick kill trigger several meters tall below the course.
- `RespawnHeightY` below every kill trigger bottom.
- Markdown result file that labels values as measured or only intended.

Do not claim the baseline is complete until the scene exists and has been validated in Unity.

## UdonSharp Script Rules

- Use `OnPlayerTriggerEnter` / `OnPlayerTriggerExit` for one-shot mechanics.
- Avoid `OnPlayerTriggerStay` for normal gameplay logic; it runs continuously while a player remains in the trigger.
- Player trigger colliders need `Is Trigger`; do not add Rigidbody just to receive VRChat player trigger events.
- Keep trigger volumes thick enough to avoid missed detection from fast falls or edge contact.
- For `TeleportTo`, use checkpoint position and rotation so respawn faces the next route. Do not use smooth local movement for VR respawn.
- Use `BehaviourSyncMode.NoVariableSync` for local-only baseline mechanics.

## Height And Avatar Scaling

Avatar scaling changes eye height, view, and body-feel. VRChat player/environment collision should not be treated as a design-variable capsule tied to avatar height.

If a test requires controlled eye height:

```csharp
player.SetAvatarEyeHeightMinimumByMeters(1.0f);
player.SetAvatarEyeHeightMaximumByMeters(1.0f);
player.SetAvatarEyeHeightByMeters(1.0f);
```

Also reapply the setting from `OnAvatarEyeHeightChanged`.

## Checkpoint Manager Shape

Use a default respawn point and monotonic checkpoint index:

```csharp
public Transform defaultRespawnPoint;
public Transform currentCheckpoint;
public int currentCheckpointIndex = -1;

public void TrySetCheckpoint(VRCPlayerApi player, Transform target, int index)
{
    if (player == null || !player.isLocal) return;
    if (target == null) return;
    if (index <= currentCheckpointIndex) return;
    currentCheckpoint = target;
    currentCheckpointIndex = index;
}
```

If using `OnPlayerRespawn` as a fallback, only redirect the local player and only after `currentCheckpoint` exists.

## Collapsing Tiles

Use local state and delayed collapse:

- `triggered` prevents repeated scheduling.
- `collapsed` or `visual.activeSelf` prevents duplicate collapse.
- `Collapse()` should check `triggered` before doing anything because delayed events cannot be canceled.
- `ResetTile()` must clear `triggered` and restore visuals/colliders.

Do not network-sync first-chapter trap tiles unless the design explicitly wants shared traps.

## Editor Scene Builders

When generating scenes with editor scripts:

- Create assets under a feature-specific folder.
- Use `AddUdonSharpComponent<T>()` for UdonSharp behaviours.
- Create or locate `UdonSharpProgramAsset` before syncing behaviours.
- Save the scene only after `CopyProxyToUdon` succeeds.
- If UdonSharp logs "has not been fully setup", wait for import/setup and rerun, or fix builder code to add UdonSharp components through the editor helper.
- Record Unity license or compile blockers explicitly instead of claiming validation.

## Validation Checklist

- Scene file exists and opens.
- Unity Console has no relevant compile errors.
- VRCSceneDescriptor has valid spawn(s) and `RespawnHeightY`.
- Movement settings explicitly set jump above zero.
- All player-triggered scripts guard local player.
- Kill triggers are thick and below course pits.
- `RespawnHeightY` is lower than kill trigger bottoms.
- Floors remain on a player-collidable layer such as Default or Environment.
- Run ClientSim, desktop, VR hardware, multiplayer, or Build & Test only when the user requests that layer or the project contract explicitly requires it for the current task.
- Do not imply that an unrequested runtime layer was exercised; do not enumerate unrelated unrun layers in routine closeout.
