# Verification

## Harness pattern
- **Ship the test code in the project**, enabled only by a system property or Gradle property (`-D<mod>.test=true`, `-P<mod>Smoke`). It is inert in normal use.
- **Server harness:** start a dev or real server headless, run the checks on ticks, write a report file with `PASS/FAIL` lines and a final `RESULT: PASS|FAIL`, then stop the server.
- **Client harness:** Fabric client gametests, or a scripted client that walks title screen → create world → join. Drive real input paths where possible (hold the actual attack `KeyMapping`, not a simulated mouse event), and capture screenshots.
- **Log scanner:** fail on any `ERROR` or `WARN` from your namespace, on "Failed to parse", "Missing", "Unknown" and "Unregistered", and on any new crash report. Allow-list known environment noise explicitly (perf counters, offline mode, auth timeouts).

## What to check
- **Load:**
  - every JSON decodes through the game's own codecs;
  - every registry entry exists;
  - every model resolves (no missing texture);
  - language key sets match (`scripts/lang_keys.py`).
- **Per item:** give it to a player, and check that it has a name and a model.
- **Weapons and tools:** attack a spawned mob and assert damage > 0. Verify each special mechanic (throwables spawn and hit, bows and crossbows fire, effects apply). Compare enchanted against unenchanted.
- **Recipes:** parse and craft each one through the recipe manager.
- **Structures:**
  - `/place structure` works for each one;
  - `/locate` finds it in the right dimension;
  - natural generation at the located spot actually builds the pieces;
  - chest loot tables resolve;
  - nothing is buried or floating.
- **World generation (golden test):** with a fixed seed and preset, sample heights, biomes and terrain types on a grid, both in the original (for example the mod's dev server) and in the port, then assert equality. Repeat per preset, and on each target server.
- **Lifecycle:** join, relog persistence, death and respawn (movement still works afterwards), dimension change, `/reload`.
- **Mixins:** a build-time audit of mixin targets and descriptors against the real jars, plus the runtime mixin audit (`MixinEnvironment.audit()`).
- **Compat:** a separate run with each optional mod loaded, checking that its feature actually engages, not just that the run doesn't crash.
- **Heights and limits:** custom dimension heights (short, vanilla, very tall); nothing placed outside the world.

## Screenshots
Capture specific views: creative tabs, first and third person, GUIs, shaders on. Look at every image before claiming success; automated asserts miss visual breakage.

## Done means
- The build passes and the harness reports `RESULT: PASS` with 0 FAIL.
- Logs are clean, and the screenshots were reviewed.
- The jar has been rebuilt from the final commit and copied for the user.
- A list of what automation did not cover goes to the user: real-client input, multiplayer with two real players, shader packs, long sessions. Ask the user to test those, and fix from their logs.
- Paste-site logs (mclo.gs, bytebin) can be fetched raw for diagnosis. Separate this project's errors from other mods' errors.
