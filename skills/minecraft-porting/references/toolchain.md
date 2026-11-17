# Toolchain

## JDK per target
| Minecraft | JDK to build and run | Bytecode target |
|---|---|---|
| 1.20.1 to 1.20.4 | 17 | 17 |
| 1.20.5 to 1.21.x | 21 | 21 |
| 26.x | 25 | 25 (mods); plugins can target 17 or 21 to also load on older servers |

Download a JDK into a gitignored `tools/` folder (Adoptium API `https://api.adoptium.net/v3/binary/latest/<ver>/ga/<os>/x64/jdk/hotspot/normal/eclipse`) instead of changing the system Java. Point builds at it with `JAVA_HOME` or `org.gradle.java.installations.paths` in the **user-level** `~/.gradle/gradle.properties`, never in the repo.

## Fabric
- **26.x is unobfuscated:**
  - use plugin id `net.fabricmc.fabric-loom` (Loom 1.18+) and no `mappings` line;
  - use `implementation` instead of `modImplementation`;
  - copy the current `fabric-example-mod` build files as the template.
- **Older versions:** use `fabric-loom` with `mappings loom.officialMojangMappings()`.
- **Get Mojang names for an intermediary-named jar** (a released 1.21.x Fabric mod). Make a throwaway Loom project for that Minecraft version with official mappings and add the jar as `modImplementation files(...)`. Loom writes a remapped copy under `.gradle/loom-cache/remapped_mods/`. Decompile that copy with Vineflower (`java -jar vineflower.jar in.jar outdir/`).
- **Decompile the target game:** run Vineflower on Loom's `minecraft-merged-*.jar` from the Gradle cache. It gives `net/minecraft/...` sources plus vanilla `data/` and `assets/`, the schema reference for JSON migrations. Keep it outside every repo.
- **Dev runs:** `runClient` and `runServer`. Add optional compat mods for tests as `compileOnly` plus a dev-only runtime dependency from `maven.modrinth:<slug>:<versionId>`, gated by a Gradle property. The default run then stays vanilla.

## Forge / NeoForge source projects
Read `build.gradle(.kts)` and `gradle.properties` for the Minecraft and loader versions, access transformers, mixin configs and Gradle-generated sources (generated language constants, for example). These generators must be reimplemented or the outputs vendored.

## Bukkit / Spigot / Paper plugins
- **Baseline:** Spigot API `compileOnly`. Add the Paper API `compileOnly` only in an isolated module or package. Ship `plugin.yml`, not `paper-plugin.yml`, so Spigot loads it. Quote `api-version`.
- **Internals (NMS):** use `paperweight-userdev` per version, or BuildTools remapped jars. 26.x needs no remapping, because Spigot and Paper share Mojang names.
- **Test servers:**
  - Paper builds come from `https://fill.papermc.io/v3/projects/paper` (versions, builds and downloads);
  - Spigot comes from BuildTools (needs git);
  - set `eula=true`, `online-mode=false` and a small view distance;
  - drive the console from a Python script: start, send commands, wait for log lines, stop.
- **Maven projects:** some require build properties, such as a non-empty branch, or they refuse to start. Read their version and branch checks before building.

## Windows pitfalls
- **"Folder in use" on rename:** usually a Gradle daemon (`gradlew --stop`), a leftover shell, an IDE or an Explorer window. If the root folder itself stays locked while children are free, move the contents (`robocopy /E /MOVE`) and delete the empty folder later.
- **Launching a GUI app from an agent shell** can leave an invisible process. Ask the user to open it.
- **Python on a managed install:** packages may live in the user site. `python -I` hides them, so run trusted local scripts without `-I`.
- **Console encoding:** call `sys.stdout.reconfigure(encoding="utf-8")` in scripts that print non-ASCII.
- **Crash reports pasted from hosts may be UTF-16.** Convert them with `iconv -f UTF-16 -t UTF-8`.
