# Orchestrating worker agents

Large ports (hundreds of files) take many hours. Run them as background workers, with the orchestrator only planning, reviewing and talking to the user.

## Brief
Use [../templates/TASK.md](../templates/TASK.md). A brief must be self-contained:
- the absolute layout, the tool paths and the build command;
- the goal and the phases;
- the hard rules (never guess APIs, licensing, local-only git);
- the exact tests that define done;
- the deliverable path;
- "keep PROGRESS.md as a precise resume point".

Add known findings as hints, such as the root causes from recon or a stack trace, so the worker doesn't rediscover them.

## Sizing workers
- **Scoped, well-specified work:** a mid-size model. Examples are a crash with a known stack, a data migration with a schema, a feature list.
- **Open-ended multi-system ports or rendering pipelines:** the strongest model.
- **Mechanical bulk translation:** a separate coding agent CLI, if one is available, to spread token budgets.

## Running
- Run workers in the background. Don't poll; wait for the completion notice.
- Tell the worker to commit after every chunk and update PROGRESS.md. An interrupted session then loses little.
- **If a worker stops with uncommitted work** (session end, quota, crash):
  1. commit it as WIP;
  2. write or patch the resume point;
  3. start a new worker from it. Hand off between agents or tools when one runs out of quota.
- **Never run two workers on the same working tree or Gradle project** at once. Sequence them, or use separate clones or worktrees.
- **Steer with messages:** for a new requirement mid-run (a rename, an extra test, "ship a preview jar as soon as X"), message the running worker instead of starting another.
- **Stop workers the user cancels**, and park any partial work on a branch rather than deleting it.

## Reviewing worker output
Don't relay claims; check them:
- rebuild;
- reread the test summary lines;
- open the screenshots;
- rerun scans (`scan_private.py`, `overlap_scan.py`, `arr_asset_audit.py`);
- check `git status` and `git log`.

Look for scope gaps: items reported as "dropped" or "deferred", and enchantments that are registered but do nothing. Either finish them or tell the user plainly.

## Progress reports to the user
Give an honest percentage with a breakdown table (done / remaining, weighted by risk; testing weighs a lot). State what is verified and what is not, separately.
