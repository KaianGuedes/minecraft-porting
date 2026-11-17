# Version pitfalls (symptom → cause → fix)

Most entries were found on 1.21.x → 26.x ports. Always confirm names against the decompiled target.

## Items, registries, data
| Symptom | Cause | Fix |
|---|---|---|
| `NullPointerException: Components not bound yet`; world creation hangs on "Preparing" | ItemStacks or `item.components()` are read during datapack reload, before components are bound | Defer capability or default building until after binding. Guard reads, and use `ItemStack.EMPTY` for placeholders. |
| "Can't find weapon type" or similar for built-in presets | Built-in entries were only added by a NeoForge registry event that no longer fires | Register the built-in presets explicitly before the data that references them loads. |
| `Unregistered key ...` from a synced-data packet, then a client disconnect with a network protocol error | The set or map is keyed by `DeferredHolder`, but packets carry the canonical `Holder.Reference` | Canonicalize every key (`deferred.getDelegate()`) on insert and lookup. |
| "Invalid player data" on join, plus "Missing registry: ResourceKey[...]" | A datapack (dynamic) registry was never registered on the new loader | Register it as a synced dynamic registry. |
| Datapack items of the same type overwrite each other's attributes | Builders share mutable maps with their preset | Copy maps per builder. |
| `ClassCastException: LocalPlayer cannot be cast to ServerPlayer`; no keybind works | A client-only factory is not registered, so the client gets the server implementation | Register the client factory in client init, after common init. |
| Player cannot move after respawn until relog | Engine still references the dead `LocalPlayer` | Hook respawn (see api-mapping) and refresh cached player references. |
| JSON fails to parse after the version bump | Data formats changed | Migrate with a script from the pristine originals, never by hand-editing outputs. See the next section. |

## 26.x data format checklist
- **`pack.mcmeta`:** `min_format`/`max_format` instead of only `pack_format`.
- **Loot tables, predicates, advancements:** `condition` → `type`; lists → a single `condition` (`all_of`); `function` → `type`; `functions` → `modifier`; typed number providers; tag entries as `#tag`.
- **Structures:** block states use `id`/`properties`; spawn `minCount`/`maxCount` → `count`.
- **Item models:** client definitions under `assets/<ns>/items/`; per-context "separate transforms" models become a `select` on `display_context` with split models (generate them at build time when the source is protected); equipment assets.
- **Renamed or removed IDs:** for example `chain` → `iron_chain`, and removed tags such as `music_discs`. Scan structure NBT for unknown block, entity or item IDs, and strip old loader-specific NBT keys, such as `forge:*` attributes.
- **Original-mod bugs:** some are silently ignored on the old version and become fatal on the new one (missing parents, missing tags, missing loot tables). Fix them, list them for the user, and keep alias choices reversible.

## Rendering (client)
| Symptom | Cause | Fix |
|---|---|---|
| Crash "Cannot sort draw with TRIANGLES" (for example opening the inventory player preview) | A translucent render type with sort-on-upload uses a TRIANGLES pipeline | Only request sorting for QUADS pipelines. |
| Exploded triangle shards with Iris or shader packs | Custom TRIANGLES copies of vanilla entity pipelines are unknown to the shader mod | Emit triangle meshes as degenerate quads (repeat the last vertex) through the *vanilla* render types. |
| Animated first-person model never shows, or another mod overrides it | The original used a removed loader event, or both mods inject at HEAD of the per-arm method | Inject at HEAD of the outer method that renders both hands (it runs before per-arm hooks), replicate the view-bob transform, and cancel when your mode is active. |
| Large compile breaks in rendering code | 26.x moved to a render-state / submit-node pipeline, a new rendering API package, and SDL input | Port renderers to submit nodes. Map key codes to SDL scancodes, and use the new input types. |

## Code and platform
| Symptom | Cause | Fix |
|---|---|---|
| Copying a vanilla class looks necessary | The vanilla class is `final` | Hold a private vanilla instance and delegate; reach private methods with `MethodHandles.privateLookupIn`. |
| Plugin crashes in a static initializer on 26.x | Version checks use `startsWith` or prefix parsing, and break on `26.3.build...` | Parse major and minor numerically. Fall back to the newest adapter instead of throwing. |
| Plugin treated as legacy | Unquoted `api-version: 1.20` is read by YAML as the float `1.2` | Quote it. |
| Compat plugin never loads | The JSON key is wrong (for example `entrypoint` vs `entrypoints`), or compat sources are excluded from the build | Check the other mod's loader code, and ship the sources and the JSON. |
| Optional integration missing at enable time | Load order | Add `softdepend` (plugins), or depends/suggests (mods). |
| "Already initialized" crash after a crash-recovery restart | One-time init throws on its second call | Make init idempotent. |
