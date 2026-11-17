#!/usr/bin/env python3
"""Detect source files that copy code from decompiled game (or other protected) sources.

For each source file, finds the decompiled file sharing the most normalized lines (stripped, longer than
--min-len chars) and reports it when the count reaches --threshold. Use --show to print the shared lines,
so imports, overridden signatures and trivial lines can be told apart from copied logic.
"""
import argparse
import os
import sys
from collections import defaultdict


def lines(path, min_len):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return {l.strip() for l in f if len(l.strip()) > min_len}
    except OSError:
        return set()


def walk(root, exts):
    for d, _, files in os.walk(root):
        for n in files:
            if n.endswith(exts):
                yield os.path.join(d, n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src_dir")
    ap.add_argument("decompiled_dir")
    ap.add_argument("--min-len", type=int, default=25)
    ap.add_argument("--threshold", type=int, default=15)
    ap.add_argument("--ext", nargs="*", default=[".java"])
    ap.add_argument("--ignore-imports", action="store_true", help="drop import/package lines before counting")
    ap.add_argument("--show", action="store_true", help="print the shared lines for each hit")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    exts = tuple(args.ext)

    index = defaultdict(set)
    for p in walk(args.decompiled_dir, exts):
        for l in lines(p, args.min_len):
            index[l].add(p)

    hits = 0
    scanned = 0
    for f in walk(args.src_dir, exts):
        s = lines(f, args.min_len)
        if args.ignore_imports:
            s = {l for l in s if not l.startswith(("import ", "package "))}
        scanned += 1
        counts = defaultdict(int)
        for l in s:
            for p in index.get(l, ()):
                counts[p] += 1
        if not counts:
            continue
        best, n = max(counts.items(), key=lambda kv: kv[1])
        if n >= args.threshold:
            hits += 1
            print(f"{n:4d}/{len(s):5d}  {os.path.relpath(f, args.src_dir)}  <->  {os.path.relpath(best, args.decompiled_dir)}")
            if args.show:
                shared = sorted(s & lines(best, args.min_len))
                for l in shared:
                    print(f"        {l[:140]}")
    print(f"files scanned: {scanned} hits: {hits}")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
