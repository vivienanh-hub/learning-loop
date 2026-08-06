#!/usr/bin/env python3
"""Consistency check for a Learning Loop workspace.

Every skill here is prose, which means nothing fails at compile time — a
command can reference a skill that doesn't exist, an issue template can seed
a title no skill looks for, and both will sit there working incorrectly for
months. This is the substitute for a type checker.

Each check exists because the corresponding bug actually shipped:

  frontmatter   an unquoted `argument-hint: [topic] | apply ...` parses as a
                YAML flow sequence and silently breaks the whole block
  commands      /lab routed to /article, which never existed
  links         relative links rot whenever a doc moves or a skill is removed
  templates     eight templates still seeded `Sheldon: ` after the rename, so
                new issues got a prefix no skill matched on
  counts        INSTALL claimed a skill count that stopped being true
  shell         a bad edit to the watcher isn't visible until it runs at 3am
  privacy       a personal city survived in a shipped instruction example

Stdlib only, no dependencies. Run from anywhere:  python3 scripts/check.py
Exit code is 0 when clean, 1 when anything failed.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Slash-commands that are referenced on purpose but have no file here: either
# they belong to Claude Code itself, or they are named in prose that explains
# why they are absent. Keep this list short and justified.
KNOWN_ABSENT = {
    "/model": "Claude Code builtin",
    "/article": "named in lab.md only to explain why the routing table was deleted",
}

# Patterns that should never appear in a public instruction file.
PRIVACY_PATTERNS = [
    (r"\bHCMC\b", "city name"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "email address"),
    (r"linkedin\.com/in/", "personal LinkedIn"),
]

WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}

problems, notes = [], []


def fail(check, msg):
    problems.append((check, msg))


def rel(p):
    return os.path.relpath(p, ROOT)


def walk(*exts, skip=(".git",)):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            if fn.endswith(exts):
                yield os.path.join(dirpath, fn)


def strip_fences(text):
    """Blank out fenced code blocks so illustrative examples aren't linted."""
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def commands():
    d = os.path.join(ROOT, ".claude", "commands")
    if not os.path.isdir(d):
        return {}
    return {fn[:-3]: os.path.join(d, fn)
            for fn in sorted(os.listdir(d)) if fn.endswith(".md")}


# ---------------------------------------------------------------- checks

def check_frontmatter(cmds):
    for name, path in cmds.items():
        text = open(path).read()
        if not text.startswith("---\n"):
            fail("frontmatter", f"{rel(path)}: no frontmatter block")
            continue
        try:
            block = text.split("---\n", 2)[1]
        except IndexError:
            fail("frontmatter", f"{rel(path)}: unterminated frontmatter")
            continue
        keys = {}
        for line in block.rstrip("\n").split("\n"):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" not in line:
                fail("frontmatter", f"{rel(path)}: not a key/value line -> {line!r}")
                continue
            k, v = line.split(":", 1)
            keys[k.strip()] = v.strip()
        if not keys.get("description"):
            fail("frontmatter", f"{rel(path)}: missing description (it is the / menu label)")
        for k, v in keys.items():
            if not v or (v[0] in "\"'" and v[-1] == v[0]):
                continue
            # Unquoted YAML: `[` opens a flow sequence, `|` opens a block scalar.
            if v.startswith("[") or v.startswith("{") or " | " in v or v.endswith(":"):
                fail("frontmatter",
                     f"{rel(path)}: `{k}: {v}` must be quoted — YAML reads it as a "
                     f"structure, not a string")


def check_commands(cmds):
    seen = {}
    for path in walk(".md", ".yml", ".yaml"):
        text = strip_fences(open(path).read())
        for m in re.finditer(r"`(/[a-z][a-z0-9-]*)`", text):
            seen.setdefault(m.group(1), set()).add(rel(path))
    for ref, where in sorted(seen.items()):
        if ref[1:] in cmds:
            continue
        if ref in KNOWN_ABSENT:
            notes.append(f"{ref} — absent on purpose ({KNOWN_ABSENT[ref]})")
            continue
        fail("commands", f"{ref} referenced in {', '.join(sorted(where))} but no such command")


def check_links():
    for path in walk(".md"):
        base = os.path.dirname(path)
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", strip_fences(open(path).read())):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.join(base, target)):
                fail("links", f"{rel(path)} -> {target} does not exist")


def check_templates(cmds):
    d = os.path.join(ROOT, ".github", "ISSUE_TEMPLATE")
    if not os.path.isdir(d):
        notes.append("no .github/ISSUE_TEMPLATE — skipped")
        return
    titles = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith((".yml", ".yaml")) or fn == "config.yml":
            continue
        path = os.path.join(d, fn)
        text = open(path).read()
        if not re.search(r"^name:\s*\S", text, re.M):
            fail("templates", f"{rel(path)}: missing name")
        m = re.search(r"^title:\s*[\"']?([^\"'\n]*)", text, re.M)
        if m:
            titles[m.group(1).strip()] = rel(path)
        for line in text.split("\n"):
            if re.match(r"^\s*(argument-hint|title):\s*\[", line):
                fail("templates", f"{rel(path)}: unquoted `{line.strip()}` breaks YAML")
    # A skill that gates on a bare title must have a template that seeds it.
    for name, path in cmds.items():
        for m in re.finditer(r"title is exactly `([^`]+)`", open(path).read()):
            want = m.group(1).strip()
            if not any(t.strip().rstrip(":") == want.rstrip(":") for t in titles):
                fail("templates",
                     f"{name}.md gates on the bare title '{want}' but no issue "
                     f"template seeds it (have: {sorted(titles)})")


def check_counts(cmds):
    path = os.path.join(ROOT, "INSTALL.md")
    if not os.path.exists(path):
        return
    text = open(path).read()
    m = re.search(r"(\w+) of the (\w+) skills reference the repo", text)
    if not m:
        notes.append("INSTALL has no skill-count sentence — skipped")
        return
    claimed_sub, claimed_tot = WORDS.get(m.group(1).lower()), WORDS.get(m.group(2).lower())
    actual_tot = len(cmds)
    actual_sub = sum(1 for p in cmds.values() if "YOUR_GITHUB_USERNAME" in open(p).read())
    if claimed_tot != actual_tot:
        fail("counts", f"INSTALL says {m.group(2)} skills; there are {actual_tot}")
    if claimed_sub != actual_sub:
        fail("counts", f"INSTALL says {m.group(1)} use the repo placeholder; "
                       f"{actual_sub} do")


def check_shell():
    for path in walk(".sh"):
        r = subprocess.run(["bash", "-n", path], capture_output=True, text=True)
        if r.returncode:
            fail("shell", f"{rel(path)}: {r.stderr.strip().splitlines()[0]}")


def check_privacy():
    for path in walk(".md", ".yml", ".yaml", ".sh"):
        text = open(path, errors="replace").read()
        for pattern, label in PRIVACY_PATTERNS:
            for m in re.finditer(pattern, text):
                if "noreply@" in m.group(0) or "example.com" in m.group(0):
                    continue
                fail("privacy", f"{rel(path)}: possible {label} -> {m.group(0)}")


# ------------------------------------------------------------------ main

def main():
    cmds = commands()
    if not cmds:
        print("no .claude/commands found — is this a Learning Loop workspace?")
        return 1

    check_frontmatter(cmds)
    check_commands(cmds)
    check_links()
    check_templates(cmds)
    check_counts(cmds)
    check_shell()
    check_privacy()

    print(f"Learning Loop check — {len(cmds)} commands in {rel(os.path.join(ROOT, '.'))}\n")
    for n in notes:
        print(f"  note  {n}")
    if notes:
        print()

    if not problems:
        print("  All checks passed.")
        return 0

    by_check = {}
    for check, msg in problems:
        by_check.setdefault(check, []).append(msg)
    for check in sorted(by_check):
        print(f"  {check}:")
        for msg in by_check[check]:
            print(f"    - {msg}")
        print()
    print(f"  {len(problems)} problem(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
