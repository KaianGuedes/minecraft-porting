# minecraft-porting

A skill for Claude Code that handles Minecraft mod and plugin ports: between loaders, between game versions, and between mods and server plugins.

```text
/plugin marketplace add KaianGuedes/minecraft-porting
/plugin install minecraft-porting@minecraft-porting
```

Prefer a manual install? Copy `skills/minecraft-porting` into `~/.claude/skills`.

## What a session looks like

You: *"Port this NeoForge 1.21.1 mod to Fabric 26.3."*

1. Claude looks at the project before touching it. It checks the source, the code and asset licenses, the size and how much of it depends on the loader, then tells you how big the job is.
2. It sets up a workspace: the original as a read-only reference, decompiled game sources for lookups, the right JDK and a resumable progress log.
3. It fixes compile errors grouped by the API that changed, checking each replacement against the real game sources.
4. It proves the result with an in-game test harness and, where possible, a comparison against the original. Then it gives you a jar plus a list of what still needs a human playtest.
5. If the port goes public, it makes sure no private data, decompiled code or protected assets end up in the repository.

Other things it is good at:
- turning a Fabric mod into a Bukkit/Spigot/Paper plugin;
- migrating datapack-heavy mods to new data formats;
- explaining a crash such as `Components not bound yet`;
- starting a new mod or plugin that targets several versions and platforms.

## Contents

**`SKILL.md`**
The workflow and its rules.

**`references/`**
Read only when the current step needs them:
- licensing and recon;
- toolchain setup;
- Forge/NeoForge to Fabric and mod to plugin API maps;
- version pitfalls, written as symptom, cause and fix;
- verification;
- running long jobs with worker agents;
- publishing.

**`templates/`**
A worker brief, a progress log and a project readme.

**`scripts/`**
Four Python checks with no dependencies:
- `scan_private.py`: personal data anywhere in git history;
- `overlap_scan.py`: code copied from decompiled game sources;
- `lang_keys.py`: translation files out of sync;
- `arr_asset_audit.py`: protected assets committed by mistake.

## Contributing

Ran into a pitfall the skill does not know about? Issues and pull requests are welcome. Describe it as the symptom you saw, the cause and the fix that worked.

## License

MIT. Minecraft is a trademark of Mojang Studios. This project is independent of Mojang, Microsoft, Anthropic and every mod loader it mentions.
