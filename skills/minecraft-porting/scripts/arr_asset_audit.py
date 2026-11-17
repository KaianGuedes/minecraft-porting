#!/usr/bin/env python3
"""Fail if a repository tracks protected upstream assets.

Checks every git-tracked file under --repo (or every file under a directory if it is not a git repo):
  * byte-identical copies of any file in the upstream assets directory;
  * paths matching --forbid globs (e.g. 'src/main/resources/assets/**', 'overlay/assets/*/models/**');
  * optional binary types that should never be committed (--forbid-ext .dll .so .dylib).
Exit code 1 on any hit.
"""
import argparse
import fnmatch
import hashlib
import os
import subprocess
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked(repo):
    r = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True)
    if r.returncode != 0:
        return [os.path.relpath(os.path.join(d, n), repo) for d, _, fs in os.walk(repo) for n in fs]
    return [p for p in r.stdout.decode("utf-8", "replace").split("\0") if p]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo")
    ap.add_argument("upstream_assets", help="directory with the protected assets, e.g. upstream/src/main/resources/assets")
    ap.add_argument("--forbid", nargs="*", default=["src/main/resources/assets/**"], help="glob patterns that must not be tracked")
    ap.add_argument("--forbid-ext", nargs="*", default=[".dll", ".so", ".dylib"])
    ap.add_argument("--skip", nargs="*", default=["upstream/*"], help="tracked paths to ignore (e.g. the submodule)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    upstream = set()
    for d, _, fs in os.walk(args.upstream_assets):
        for n in fs:
            upstream.add(sha(os.path.join(d, n)))

    hits = []
    files = tracked(args.repo)
    for rel in files:
        rel = rel.replace("\\", "/")
        if any(fnmatch.fnmatch(rel, s) for s in args.skip):
            continue
        full = os.path.join(args.repo, rel)
        if not os.path.isfile(full):
            continue
        if any(fnmatch.fnmatch(rel, g) for g in args.forbid):
            hits.append(f"forbidden path: {rel}")
        elif rel.lower().endswith(tuple(args.forbid_ext)):
            hits.append(f"forbidden binary: {rel}")
        elif sha(full) in upstream:
            hits.append(f"identical to an upstream asset: {rel}")
    for h in hits:
        print(h)
    print(f"checked {len(files)} files against {len(upstream)} upstream assets: {len(hits)} hits")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
