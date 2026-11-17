#!/usr/bin/env python3
"""Check translation files for key-set and placeholder parity against a base language.

Supports .json (Minecraft lang) and .yml/.yaml (flat or nested; parsed with PyYAML if installed,
otherwise a simple built-in reader for 'key: value' and nested indentation). Reports missing keys, extra
keys, empty values and placeholder mismatches (%s, %1$s, %name%, {0}, {name}, MiniMessage tags, &a / §a codes).
Usage arguments such as <player> are treated as translatable text, not placeholders.
"""
import argparse
import json
import os
import re
import sys

PH = re.compile(r"%\d*\$?[sdf]|%[A-Za-z_]+%|\{[A-Za-z0-9_]*\}|[&§][0-9a-fk-or]", re.IGNORECASE)
TAG = re.compile(r"</?(?:#[0-9a-f]{6}|[a-z_]+(?::[^>]*)?)>", re.IGNORECASE)
MM_TAGS = {"bold","italic","underlined","strikethrough","obfuscated","reset","gradient","rainbow","hover","click","color","font","lang","key","newline","br","red","green","blue","yellow","gold","aqua","gray","grey","dark_gray","white","black","dark_red","dark_green","dark_blue","dark_aqua","dark_purple","light_purple"}


def placeholders(text):
    found = PH.findall(text)
    found += [t for t in TAG.findall(text) if t.strip("</>").split(":")[0].lower() in MM_TAGS or t.startswith(("<#", "</#"))]
    return sorted(found)


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = "" if v is None else (json.dumps(v, ensure_ascii=False) if isinstance(v, list) else str(v))
    return out


def simple_yaml(text):
    root = {}
    stack = [(-1, root)]
    last = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        if stripped.startswith("- ") or stripped == "-":
            if last is not None:
                parent, key = last
                if not isinstance(parent.get(key), list):
                    parent[key] = []
                parent[key].append(stripped[1:].strip().strip("'\""))
            continue
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip().strip("'\"")
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        val = val.strip()
        if val == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
            last = (parent, key)
        else:
            parent[key] = val.strip("'\"")
            last = None
    return root


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.endswith(".json"):
        return flatten(json.loads(text))
    try:
        import yaml
        return flatten(yaml.safe_load(text) or {})
    except ImportError:
        return flatten(simple_yaml(text))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lang_dir")
    ap.add_argument("--base", default="en_us", help="base file name without extension (en_us, en-US, ...)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    files = {os.path.splitext(n)[0]: os.path.join(args.lang_dir, n) for n in os.listdir(args.lang_dir)
             if n.endswith((".json", ".yml", ".yaml"))}
    base_name = next((k for k in files if k.lower() == args.base.lower()), None)
    if not base_name:
        sys.exit(f"base language '{args.base}' not found in {args.lang_dir}")
    base = load(files[base_name])
    problems = 0
    for name, path in sorted(files.items()):
        if name == base_name:
            continue
        try:
            data = load(path)
        except Exception as e:
            print(f"{name}: PARSE ERROR {e}")
            problems += 1
            continue
        missing = sorted(set(base) - set(data))
        extra = sorted(set(data) - set(base))
        empty = sorted(k for k, v in data.items() if not str(v).strip())
        ph = sorted(k for k in set(base) & set(data) if placeholders(base[k]) != placeholders(data[k]))
        n = len(missing) + len(extra) + len(empty) + len(ph)
        problems += n
        status = "OK" if n == 0 else f"{n} problem(s)"
        print(f"{name}: {status}")
        for label, keys in (("missing", missing), ("extra", extra), ("empty", empty), ("placeholders", ph)):
            for k in keys[:50]:
                print(f"   {label}: {k}")
    print(f"base {base_name}: {len(base)} keys, {len(files) - 1} other files, {problems} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
