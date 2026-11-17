#!/usr/bin/env python3
"""Scan every commit (tree and message) of a git repo for private data before publishing.

Default patterns catch absolute user paths and email addresses. Add your own with --patterns
(usernames, real names, private folder names). Exit code 1 if anything is found.
"""
import argparse
import re
import subprocess
import sys

DEFAULT = [
    r"[A-Za-z]:\\\\?Users\\\\?[^\\\s\"'<>]+",
    r"/(?:c|d)/Users/[^/\s\"'<>]+",
    r"/home/[a-z_][a-z0-9_-]*",
    r"/Users/[A-Za-z0-9_.-]+",
    r"AppData[\\/]",
    r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
]


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo")
    ap.add_argument("--refs", nargs="*", default=["--all"], help="refs to scan (default: --all)")
    ap.add_argument("--patterns", nargs="*", default=[], help="extra case-insensitive regexes or literals")
    ap.add_argument("--no-defaults", action="store_true", help="only use --patterns")
    ap.add_argument("--exclude", nargs="*", default=[], help="pathspecs to skip, e.g. upstream")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pats = ([] if args.no_defaults else DEFAULT) + args.patterns
    rx = re.compile("|".join(f"(?:{p})" for p in pats), re.IGNORECASE)
    revs = git(args.repo, "rev-list", *args.refs).split()
    hits = set()
    for rev in revs:
        msg = git(args.repo, "log", "-1", "--format=%an <%ae>%n%cn <%ce>%n%B", rev)
        for line in msg.splitlines():
            if rx.search(line):
                hits.add(f"{rev[:8]} [message/author] {line.strip()[:160]}")
        spec = ["--", "."] + [f":!{e}" for e in args.exclude]
        out = git(args.repo, "grep", "-nIiE", rx.pattern, rev, *spec)
        for line in out.splitlines():
            hits.add(f"{rev[:8]} {line.split(':', 1)[1][:200] if ':' in line else line}")
    for h in sorted(hits):
        print(h)
    print(f"scanned {len(revs)} commits, {len(hits)} hits")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
