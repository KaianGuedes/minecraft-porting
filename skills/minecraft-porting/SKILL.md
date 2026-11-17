---
name: minecraft-porting
description: Port Minecraft mods and plugins between loaders (Forge, NeoForge, Fabric, Quilt), between Minecraft versions (including the unobfuscated 26.x line), from a client/server mod to a Bukkit/Spigot/Paper server plugin or back, migrate datapack-heavy mods, rebuild a mod from a decompiled or open-source base, and create new mods or plugins with a cross-version, cross-platform architecture. Use when the user asks to port, update, convert, rebuild or create a Minecraft mod/plugin/datapack, or to fix a port that crashes, fails to compile or behaves differently from the original.
---

# Minecraft porting

A repeatable method for porting and building Minecraft mods and plugins. It covers recon, licensing, toolchain, API mapping, version pitfalls, verification, worker orchestration and publishing. Read the reference file for the phase you are in; do not load everything at once.

| Phase | Read |
|---|---|
| Recon, license, can it be published? | [references/recon-and-licensing.md](references/recon-and-licensing.md) |
| JDK, Gradle/Loom/Maven, decompiling, test servers | [references/toolchain.md](references/toolchain.md) |
| Translating loader or platform APIs | [references/api-mapping.md](references/api-mapping.md) |
| Crashes and behaviour changes after a version jump | [references/version-pitfalls.md](references/version-pitfalls.md) |
| Proving the port works | [references/verification.md](references/verification.md) |
| Long jobs with worker agents | [references/orchestration.md](references/orchestration.md) |
| Repos, releases, platform listings | [references/publishing.md](references/publishing.md) |

Templates: [templates/TASK.md](templates/TASK.md) (worker brief), [templates/PROGRESS.md](templates/PROGRESS.md) (public-safe progress log), [templates/README.md](templates/README.md).
Scripts (Python, stdlib only, run with `--help`): `scripts/scan_private.py`, `scripts/overlap_scan.py`, `scripts/lang_keys.py`, `scripts/arr_asset_audit.py`.

## Workflow

1. **Recon.** Before writing code, answer:
   - Is source available (repo, branch per version), or only a jar?
   - What are the licenses, separately for the code and for the assets?
   - Which loader and version is the source, and which is the target?
   - How big is it? Count Java files and lines, files importing loader APIs, mixins, and data files (structures, JSON).
   - Is it code-heavy, data-heavy or rendering-heavy?

   Report these to the user with a rough effort estimate. Recon is cheap and decides everything else.
2. **Classify the job:**
   - version bump on the same loader;
   - loader swap;
   - mod to plugin, or plugin to mod;
   - datapack or data migration;
   - new project.

   Mixed jobs (a loader swap plus a version jump) are the hardest. Say so.
3. **Set up the workspace:**
   - one folder per project, with a local git repo from the first minute;
   - `upstream/`: the original source, read-only, as a clone or a submodule;
   - a decompiled target-version game source tree, used only for lookups and never committed;
   - the right JDK, a gitignored `TASK.md` brief and a `PROGRESS.md` resume log.
4. **Port by root cause.**
   - Compile early, then group errors by the API that changed. One rename often explains hundreds of errors.
   - Fix whole packages at a time.
   - Check every class, method, descriptor, codec and JSON schema against the decompiled target sources or vanilla data. Never guess.
   - If the target version already provides a system natively (item components, data-driven enchantments, registries), rewriting onto it is often simpler than translating the old code. Keep the original behaviour and IDs.
5. **Prove it.** "It compiles" is not done. Build an automated harness: a client or server smoke run behind a `-D` flag. Then:
   - compare against the original (a golden test) when one is runnable;
   - test every item, recipe, structure and mechanic;
   - open the screenshots yourself;
   - require clean logs.

   Then hand the user a jar and ask for a real-player test of whatever automation cannot reach.
6. **Ship:**
   - comply with the licenses;
   - keep private data and copied game code out of history;
   - write the README and release notes;
   - set the correct release channel and platform metadata.

## Rules

- **Never guess an API.** Look it up in the decompiled target sources or the dependency jar.
- **Never publish decompiled game code**, or vanilla implementations copied and lightly edited. Extend, delegate to a vanilla instance, or use reflection or method handles instead. Run `scripts/overlap_scan.py` before pushing.
- **Never commit All Rights Reserved assets**, or files mechanically derived from them. Assemble them at build time from a submodule and generate derived files during the build. Run `scripts/arr_asset_audit.py`.
- **All Rights Reserved mods are personal-use ports only.** Keep them in local git, never pushed or redistributed.
- **Keep `PROGRESS.md` public-safe and current.** Any agent must be able to resume from it.
- **Don't run two workers on the same working tree** at once.
- **Verify worker claims yourself before reporting success:** rebuild, reread the test summary and open the images.
- **Preserve compatibility identifiers** when renaming a fork, so datapacks, resource packs and worlds keep working: resource namespace, registry IDs and command roots. Change the code package and the platform mod or plugin id instead.
