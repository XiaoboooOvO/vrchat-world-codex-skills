# Generated Content Workflow

Use this reference for authoring tools, schemas, importers, catalogs, atlases,
shader includes, Bake steps, or any pipeline that turns editable content into
Unity runtime assets.

## Map the one-way truth flow

Identify these roles before editing:

```text
authoring source
  -> validation and review state
  -> importer or generator
  -> generated Unity assets
  -> serialized scene or prefab references
  -> runtime consumers
```

Keep generated artifacts reproducible from their declared source. Do not repair a
generated file by hand when the next import will overwrite it. Do not reconstruct
authoring data from a catalog, scene array, atlas, or shader include unless the
project explicitly defines that reverse operation.

## Separate lifecycle states

Keep prototype, reviewed, approved, imported, generated, and published states
distinct. Renaming an ID or copying a file does not promote content. Formalization
must validate the source identity, required pairs or dependencies, review state,
stable identifier, and collision with existing content before writing anything.

When a requested batch exceeds a frozen tool contract, split the work into
supported batches. Do not widen schema or importer behavior merely to fit one run.

## Validate assets at the source boundary

For external or raster source assets, verify the project-approved path, content
hash when used, original dimensions, import settings, crop, opacity, orientation,
and intended runtime role. Treat authoring guides, previews, and final runtime
assets as separate surfaces.

Repair systemic generation defects in the generator and keep a defensive importer
or Bake check when silent data loss would otherwise remain possible. Add a focused
regression for affected and unaffected content.

## Prepare localized TMP glyphs as generated content

Treat localized strings and their TextMesh Pro atlas as a one-way generated-content
flow:

```text
authoritative text
  -> imported or serialized content
  -> required-character collector
  -> existing TMP_FontAsset
  -> atlas and material assets
  -> runtime text consumers
```

For Chinese, Japanese, or other non-ASCII static text:

- Import or synchronize the authoritative strings before collecting characters
  when the collector reads Unity authoring or catalog data.
- Use the project-owned Editor entry point or generator. Do not hand-edit atlas
  textures or replace the font asset merely to add glyphs.
- Compute the unique required-character set, identify missing glyphs, and add only
  the missing set.
- Preserve the existing `TMP_FontAsset` path, GUID, material, fallback chain, and
  serialized references.
- If the established tool temporarily enables dynamic or multi-atlas population,
  restore the project-required runtime mode, often `Static`, before saving.
- Persist a compact result reporting required, added, and still-missing glyph
  counts. Require zero missing glyphs and check for new Console errors.
- Do not rely on runtime dynamic generation to conceal missing build-time glyphs.
  Keep dynamic player names or client fallback fonts separate from static
  localized content.

## Treat import and Bake as durable runs

Use a stable run identity for operations that can trigger import, atlas rebuild,
domain reload, or connection loss. A terminal result should identify the inputs,
changed targets, final status, and stable post-save state.

Do not interpret menu return, timeout, disconnect, `STARTED`, or `PENDING` as
success. Do not repeat the action until the same run is known to be terminal.

Use the routine project entry point for ordinary content. Expand to schema,
importer, Bake, runtime, or broad regression work only when the requested change
actually crosses those boundaries.
