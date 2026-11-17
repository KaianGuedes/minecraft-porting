# API mapping

## Forge / NeoForge → Fabric
| Forge / NeoForge | Fabric |
|---|---|
| Event bus subscribers (`@SubscribeEvent`) | Fabric API callbacks (`ServerLifecycleEvents`, `ServerEntityEvents`, `ServerPlayerEvents`, `ClientTickEvents`, `HudElementRegistry`, ...). If there is none, add a mixin that fires your own event |
| Capabilities / data attachments | Fabric Data Attachment API (`AttachmentRegistry`, `AttachmentTarget.getAttachedOrCreate`) |
| `DeferredRegister` / `RegistryObject` / `DeferredHolder` | static `Registry.register` at init. A small DeferredRegister-style adapter keeps the code shape, but resolve holders canonically (see version-pitfalls) |
| Custom registries | `FabricRegistryBuilder`; sync where needed |
| `DataPackRegistryEvent.NewRegistry` | `DynamicRegistries.registerSynced(key, codec)` |
| `SimpleChannel` / `CustomPacketPayload` handlers | `PayloadTypeRegistry` plus `ServerPlayNetworking` / `ClientPlayNetworking` |
| `ModConfigSpec` | A JSON config with typed defaults and range checks, or a Fabric-friendly config library |
| Access transformers | Access wideners / class tweakers |
| `ClientPlayerNetworkEvent.Clone` (respawn) | Mixin on `ClientPacketListener.handleRespawn`: capture the old player at HEAD, call the hook at RETURN |
| `RenderHandEvent` | Mixin on the first-person hand renderer, on the method that renders both hands (see version-pitfalls) |
| Entity attribute creation/modification events | `FabricDefaultAttributeRegistry` / attribute modification callbacks |
| Reload listeners | `ResourceLoader` / `ResourceManagerHelper` reload listeners |
| `enqueueWork` / client setup | `onInitializeClient`. Register client-only factories (for example a local-player patch) there, after common init |
| Mod container lookups by mod id | `FabricLoader.getModContainer`. If the fork changes the mod id but keeps the resource namespace, use two constants: `MOD_ID` for loader lookups and `NAMESPACE` for resources, registries and packets |

Compat with other mods: discover them the way the other mod expects. For example, a mod may scan every mod's `<modid>_plugin.json` for an `entrypoints` key. Compile compat as `compileOnly` and load it only when the mod is present.

## Fabric mod → Bukkit / Spigot / Paper plugin
| Mod | Plugin |
|---|---|
| Mixins into vanilla | a per-version NMS module plus a Bukkit API fallback chosen at runtime; or Bukkit events when they exist |
| Custom chunk generator / noise router hooks | NMS: a generator that *delegates* to the vanilla noise generator (it is final), installed when the world is created. Fallback: `ChunkGenerator` (`generateNoise/Surface/Bedrock/Caves`), `BiomeProvider`, `BlockPopulator` + `LimitedRegion`, `getBaseHeight`, and `shouldGenerate*` to keep vanilla/datapack/other-plugin structures |
| Client screens (world creation tab, editors, live map) | files (keep the mod's file format so presets are interchangeable), commands, and exported PNG previews |
| Mod config | `config.yml` |
| Client-side rendering | not available; use vanilla features or resource packs |

**Runtime feature detection.** Probe for a class that exists only on Paper (`Class.forName`), and keep Paper-only code in separate classes behind an interface, loaded only when detected. Do the same for NMS: pick the module matching the server version, else fall back. The same jar then runs on Spigot, Paper and Purpur. Folia needs region-aware scheduling; mark it unsupported unless that is implemented.

## Plugin → mod
Do the reverse:
- Bukkit events become Fabric callbacks or mixins.
- `plugin.yml` commands become Brigadier commands.
- YAML config becomes JSON or YAML via a library.
- Persistent data containers become data attachments.
- The scheduler becomes server tick events.

## Architecture for new multi-version projects
- **Modules:**
  - `core`: pure Java, no game or loader imports;
  - `<platform>`: an adapter for each platform (Fabric, Bukkit);
  - `<platform>-v<mc>`: per-version modules;
  - `plugin` or `mod`: the final shaded jar.
- **Branding:** keep the display name, data folder, command root and jar name in **one constant**, generated from `gradle.properties`, so a rename is one line.
- **Compatibility aliases:** keep old command aliases and permission nodes, and migrate old data folders and configs automatically, with a backup.
- **Localisation:** language files with identical key sets. `language: auto` picks the player locale, then the language prefix, then the server default, then English.
