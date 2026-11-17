# <Project> progress

> Public-safe progress log. Never write local paths, usernames, emails, tokens, API keys,
> server IPs or private repo URLs here. Use repo-relative paths and placeholders (`<JDK>`, `<HOME>`).
> Machine-specific notes go in a gitignored TASK.md.

**Status:** `IN PROGRESS` | `DONE` | `BLOCKED`
**Target:** <loader> <Minecraft version> (Java <N>)
**Based on:** <upstream project> `<commit or version>` (<license>)

## Summary
One short paragraph: what works today and what does not.

## Milestones
| # | Milestone | Status | Notes |
|---|---|---|---|
| 1 | Builds | ✅ | |
| 2 | Loads / reaches title screen or server start | ✅ | |
| 3 | Core gameplay | 🚧 | |
| 4 | Compatibility | ⏳ | |

Legend: ✅ done, 🚧 in progress, ⏳ not started, ⛔ blocked.

## Changes
Group by area. One line per change, with the reason when it is not obvious.

### <Area>
- <What changed>. <Why>.

## Fixes
| Issue | Root cause | Fix | Verified by |
|---|---|---|---|
| <symptom> | <cause> | <fix> | <test / screenshot> |

## Not ported / known limitations
- <Feature>: <reason>, <workaround if any>.

## Verification
| Check | Result |
|---|---|
| `<build command>` | PASS |
| <harness> | PASS (<counts>) |

## How to reproduce the tests
```sh
<build command>
<test commands, using environment variables instead of local paths>
```

## Resume point
<Exact next step for whoever continues: file, failing test, open question.>

## Next steps
1. <next task>
