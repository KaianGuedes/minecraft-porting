# Worker brief: <project> (<source loader/version> → <target loader/version>)

> Local, gitignored. Machine-specific paths belong here, never in tracked files.

## Layout
- Repo: `<absolute path>` (local git; <push policy>)
- `upstream/`: original source, read-only reference (branch/commit `<ref>`)
- Decompiled target game sources and vanilla data: `<absolute path>` (lookups only, never copy)
- JDK: `<absolute path>`; build: `<command>`
- Template project for the target toolchain: `<absolute path or repo>`
- Reference ports with the same jump: `<paths>` (see their PROGRESS.md)

## Goal
<One paragraph: what must work at the end, which versions/platforms, what must stay compatible (namespace, IDs, configs, worlds).>

## Known findings
- <recon facts, root causes already identified, stack traces, user decisions>

## Rules
- Verify every API, descriptor, codec and data schema against the decompiled target sources. Never guess.
- No copied game code and no protected assets in tracked files.
- Keep original behaviour; stub only what truly has no equivalent, and list each stub with its reason.
- Commit after every meaningful chunk and keep PROGRESS.md as a precise resume point.
- <project-specific rules: license notices, naming, docs style, commit format>

## Phases
1. <skeleton / build setup>
2. <compile: port by root cause, package by package>
3. <data / assets migration>
4. <client / rendering>
5. <compat>
6. <tests and fixes until clean>

## Tests (all must pass)
- `<build command>` passes, including audits.
- Harness `<command or -D flag>` reports `RESULT: PASS` with 0 FAIL, covering: <items / recipes / structures / mechanics / lifecycle / golden comparison>.
- Logs show no errors or warnings from the project's namespace; screenshots `<list>` captured and reviewed.

## Deliverable
- Jar: `<build/libs/...>` copied to `<path>`.
- PROGRESS.md says DONE with an evidence table.

## Final report (short)
What was done, what was stubbed and why, test counts, jar path, anything left.
