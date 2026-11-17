# Publishing

## Before the first push
- **Personal data:** run `scripts/scan_private.py <repo> --patterns <username> <email> ...` over **all commits and messages**. Local absolute paths, usernames and emails leak easily into build files, test scripts, logs and docs. Replace them with environment variables or user-level config, and scrub logs to `<HOME>`.
- **Private notes:** worker briefs (`TASK.md`), progress logs containing private notes, test servers, run directories, decompiled sources, IDE folders and tool downloads belong in `.gitignore`. Keep public `PROGRESS.md` files public-safe ([../templates/PROGRESS.md](../templates/PROGRESS.md)).
- **Copied code and assets:** run `overlap_scan.py` and `arr_asset_audit.py`.
- **Commit identity:** use the hosting provider's no-reply email if the author's personal email should stay private.
- **History rewrites, when needed:**
  1. `git bundle create backup.bundle --all`;
  2. `git filter-branch` with `--tree-filter`, `--index-filter`, `--env-filter` or `--msg-filter`;
  3. delete `refs/original` and any backup branches that still hold old history;
  4. rescan.

  Note that `--index-filter git rm --cached` also deletes the files from the working tree, so copy them first.
- **Force-pushing a public repo** needs explicit consent. Explain that clones and caches keep the old commits, and that the host may need a cache purge request.

## Releases
- **Tags:** follow the project's convention, for example `<version>_<mc range>` such as `0.3.0_1.20+`. Use annotated tags whose message is the release title.
- **Release notes:** a short intro, then grouped changes, then **Breaking changes / Read before updating** (changed command syntax, defaults now off, moved config keys, data migrations), then known limitations, credits, and a changelog compare link. Remove assistant chatter from generated notes. Describe a 0.x → 0.y bump as minor.
- **Channel:** a first public version that has only passed automated tests is **beta**. Use release after real-world use without serious bugs. Alpha is for incomplete or risky builds.
- **Release builds:** rebuild the jar from the exact tagged commit before attaching it.

## Platform listings
- **Modrinth loaders:** tick only what was tested or is binary-compatible:
  - Paper, Spigot, and Purpur (a Paper fork);
  - not Folia unless supported;
  - not Bukkit unless tested on CraftBukkit;
  - never the proxies (BungeeCord, Velocity, Waterfall) for a game-server plugin.
- **Slugs:** if the display name's slug is taken (possibly by a private project the API can't show), keep the name and choose a descriptive slug such as `<name>-worldgen`. Reserve it early with a draft.
- **Categories:** pick the one or two that describe the main function. Extra categories hurt relevance.
- **Name collisions:** search Modrinth, Hangar, SpigotMC and CurseForge. The API only shows public projects.
- **AI content rules:** see recon-and-licensing.md. Disclose the AI use, use a human-made icon, and expect review for AI-heavy projects. Have fallbacks: GitHub Releases, Hangar, SpigotMC.

## Project metadata
- **README:** [../templates/README.md](../templates/README.md). Cover what it is, compatibility, installation, configuration, commands and permissions, limitations, building, credits, and license.
- **Credits:** credit every upstream author, and state that the project is not endorsed by them.
- **License files:** include LICENSE, and a NOTICE where required.
