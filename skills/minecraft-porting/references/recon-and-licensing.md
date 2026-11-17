# Recon and licensing

## Recon checklist
- **Source:** look for a GitHub/GitLab link on the project page (Modrinth API `source_url`). Upstream often has an unreleased branch for the version you want; check `git ls-remote --heads`. Before porting, check whether upstream master already supports the target (for example a `LATEST_VERSION` constant). Sometimes the "port" is only a build.
- **Versions and loaders:** use the Modrinth API to list versions: `GET /v2/project/<slug>/version?loaders=["fabric"]&game_versions=["26.3"]`.
- **Size metrics:**
  - Java file and line count;
  - files importing loader packages (`net.neoforged`, `net.minecraftforge`, `net.fabricmc`);
  - `net.minecraft` imports in a "common" module, which shows how coupled it is;
  - mixin count;
  - structure `.nbt` and JSON counts.
- **Classify the effort:**
  - data-heavy, with few classes: schema migration plus tests;
  - code-heavy, with loader APIs everywhere: a big translation;
  - rendering-heavy: the riskiest, because render pipelines change often.

## License decision table
| License | Port for yourself | Publish a modified port | Notes |
|---|---|---|---|
| All Rights Reserved | yes | no | Local git only. Don't push, don't redistribute the jar. |
| MIT | yes | yes | Keep the copyright and license text of every original author. |
| Apache-2.0 | yes | yes | Keep LICENSE, add a NOTICE describing your changes. |
| GPL-3.0 / LGPL-3.0 | yes | yes | Same license, source must be published. LGPL also allows linking. |
| Artistic-2.0 | yes | conditionally | Modified redistributions must be clearly marked or renamed. |
| CC-BY-NC-SA | yes | yes, non-commercial | Attribution, same license, no selling. |
| Custom (e.g. "Abnormals License", per-mod licenses) | read it | read it | Public source does not mean redistributable. |

Always check **code vs assets** separately. A repo can be GPL for code and All Rights Reserved for `assets/` (textures, models, animations, sounds, translations, shaders, native libraries). Read the README for explicit fork terms, such as "assets replaced, different name, credit, grant-back".

## Shipping a fork whose assets are All Rights Reserved
- **Do:**
  - add the original repo as a git **submodule** pinned to a commit;
  - copy its assets into the build output at build time;
  - apply your own `overlay/` on top: new files you wrote, such as new-format item definitions;
  - merge language files key by key, so the overlay contains only new keys.
- **Generate derived files at build time.** Examples are per-context models split from an upstream model, or re-encoded data. Never commit them.
- **A GitHub fork is not a workaround.** It copies the full history, assets included, publicly.
- **The built jar still contains the assets.** The repo can be public, but the jar is personal use unless the asset owner allows redistribution.
- **Remove online services that talk to the original project's servers.** Examples are accounts, cosmetics and update checks, especially anything that sends player tokens. Multiplayer is unaffected.

## Game code
Decompiled game source is for lookups only. Never commit it, and never paste a vanilla class into your code and then edit it. If the class is final, delegate to a vanilla instance and reach private members via reflection or `MethodHandles.privateLookupIn`. Check with `scripts/overlap_scan.py`: what remains should be only imports, overridden method signatures and trivial lines.

## Platform rules about generative AI (check current rules before publishing)
Some platforms, Modrinth among them, require:
- an "AI-generated content" disclosure when substantial code, assets or the project page come from AI;
- no AI-generated images in icons, galleries or descriptions;
- projects made primarily of AI output to stay unlisted.

Tell the user before they upload. The icon must be human-made, and disclosure is mandatory.
