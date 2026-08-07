#!/usr/bin/env python3
"""Consistency check for a Learning Loop workspace.

Every skill here is prose, which means nothing fails at compile time — a
command can reference a skill that doesn't exist, an issue template can seed
a title no skill looks for, and both will sit there working incorrectly for
months. This is the substitute for a type checker.

Each check exists because the corresponding bug actually shipped:

  frontmatter   an unquoted `argument-hint: [topic] | apply ...` parses as a
                YAML flow sequence and silently breaks the whole block; a
                duplicate key is resolved last-one-wins and hides the other
  commands      /lab routed to /article, which never existed
  links         relative links rot whenever a doc moves or a skill is removed
  templates     eight templates still seeded `Sheldon: ` after the rename, so
                new issues got a prefix no skill matched on
  counts        INSTALL claimed a skill count that stopped being true
  threshold     a blog draft compressed "three independent episodes" into
                "three or more sessions" — the same number, a different rule
  orphans       docs/memory-setup.md specified the founding records correctly
                and nothing linked to it, so INSTALL contradicted it unnoticed
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
#
# A workspace can add its own, one `/name  reason` per line, in
# scripts/check-allow.txt — retired skills stay named in planning docs long
# after the file goes, and that is correct, not rot.
KNOWN_ABSENT = {
    "/model": "Claude Code builtin",
    "/article": "named in lab.md only to explain why the routing table was deleted",
}

# Dated evidence. These hold what was true when written and must not be
# rewritten to match the present, so they are exempt from reference and
# privacy checks. See docs/memory-policy.md — correction leaves an audit
# trail rather than editing history.
HISTORICAL = (".claude/memory", "journal")

# The memory policy is the source of the one threshold everything else
# restates. A published subset carries it in docs/; the private workspace it
# was extracted from carries it in system/. Same file, same rules, and this
# script has to run in both.
POLICY_LOCATIONS = ("docs/memory-policy.md", "system/memory-policy.md")

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


def walk(*exts, skip=(".git",), historical=True):
    """Yield files. historical=False omits dated-evidence directories."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip]
        if not historical and rel(dirpath).startswith(HISTORICAL):
            continue
        for fn in filenames:
            if fn.endswith(exts):
                yield os.path.join(dirpath, fn)


def load_allowlist():
    """Read scripts/check-allow.txt. `/name reason` allows a missing command;
    `!check reason` disables a whole check (privacy is meant for repos that
    will be public — a private workspace should switch it off deliberately)."""
    allow, disabled = dict(KNOWN_ABSENT), {}
    path = os.path.join(ROOT, "scripts", "check-allow.txt")
    if os.path.exists(path):
        for line in open(path):
            line = line.split("#")[0].strip()
            if not line:
                continue
            name, _, reason = line.partition(" ")
            reason = reason.strip() or "set in scripts/check-allow.txt"
            (disabled if name.startswith("!") else allow)[name.lstrip("!")] = reason
    return allow, disabled


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
            k = k.strip()
            # A repeated key is silently resolved by every YAML parser — last
            # one wins — so a stale line can sit above a corrected one doing
            # nothing visible until the order changes.
            if k in keys:
                fail("frontmatter", f"{rel(path)}: duplicate key `{k}` — one of them is dead")
            keys[k] = v.strip()
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
    allow, _ = load_allowlist()
    seen = {}
    for path in walk(".md", ".yml", ".yaml", historical=False):
        text = strip_fences(open(path).read())
        for m in re.finditer(r"`(/[a-z][a-z0-9-]*)`", text):
            seen.setdefault(m.group(1), set()).add(rel(path))
    for ref, where in sorted(seen.items()):
        if ref[1:] in cmds:
            continue
        if ref in allow:
            notes.append(f"{ref} — absent on purpose ({allow[ref]})")
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
    install = os.path.join(ROOT, "INSTALL.md")
    if os.path.exists(install):
        text = open(install).read()
        m = re.search(r"(\w+) of the (\w+) skills reference the repo", text)
        if not m:
            notes.append("INSTALL has no skill-count sentence — skipped")
        else:
            claimed_sub = WORDS.get(m.group(1).lower())
            claimed_tot = WORDS.get(m.group(2).lower())
            actual_tot = len(cmds)
            actual_sub = sum(1 for p in cmds.values()
                             if "YOUR_GITHUB_USERNAME" in open(p).read())
            if claimed_tot != actual_tot:
                fail("counts", f"INSTALL says {m.group(2)} skills; there are {actual_tot}")
            if claimed_sub != actual_sub:
                fail("counts", f"INSTALL says {m.group(1)} use the repo placeholder; "
                               f"{actual_sub} do")

    # The README opens by inventorying the repo. Removing /cv-job-match took the
    # command count down and left the script count beside it untouched, so the
    # first substantive line of the repo was wrong for four commits.
    readme = os.path.join(ROOT, "README.md")
    if not os.path.exists(readme):
        return
    m = re.search(r"(\w+) slash commands, (\w+) shell scripts", open(readme).read())
    if not m:
        notes.append("README has no inventory sentence — skipped")
        return
    for claimed, actual, label in (
        (m.group(1), len(cmds), "slash commands"),
        (m.group(2), sum(1 for _ in walk(".sh")), "shell scripts"),
    ):
        if WORDS.get(claimed.lower(), claimed) != actual:
            fail("counts", f"README says {claimed} {label}; there are {actual}")


def check_threshold():
    """The memory threshold is stated in prose in several places on purpose —
    the README has to say the number, and so does a blog post. What must not
    happen is a restatement drifting off the policy: "three or more sessions"
    is the same number and a materially weaker rule, because it drops the
    independence requirement that stops one bad day counting three times.

    So this reads the canonical rule out of docs/memory-policy.md and checks
    every restatement against it, rather than banning restatement."""
    policy = next((p for p in (os.path.join(ROOT, *loc.split("/"))
                               for loc in POLICY_LOCATIONS) if os.path.exists(p)), None)
    if policy is None:
        notes.append("no memory policy found — threshold check skipped")
        return
    canon = re.search(r"(\w+)\s+\*\*independent\*\*\s+episodes", open(policy).read())
    if not canon:
        fail("threshold", f"{rel(policy)} no longer states 'N **independent** "
                          f"episodes' — nothing else can be checked against it")
        return
    want = canon.group(1).lower()

    # A restatement is a count of things that could promote a claim about the
    # learner. Two narrowings keep this off ordinary prose. The count must be
    # introduced by a word that makes it a requirement ("after three
    # episodes"), so "220 sessions logged as issues" in a list of activity
    # totals is not a threshold just because the sentence also says "memory".
    # And the line must already be about promotion, so "three attempts" in
    # exam.md and "three chunks" in learn.md never come near it.
    trigger = (r"(?:after|across|over|within|in|needs?|requires?|takes?|"
               r"seen\s+in|shows?\s+up\s+(?:in|across)|promoted\s+(?:after|from))")
    counted = r"(?:episodes?|sessions?|occurrences?|instances?|observations?)"
    restated = re.compile(
        trigger + r"\s+\b(" + "|".join(WORDS) + r"|\d+)\b"
        r"((?:\s+(?:or\s+more|\*{0,2}independent\*{0,2}|separate|distinct))*)\s+"
        + counted, re.I)
    context = re.compile(r"promot|candidate|durable|infer|pattern memory|memory", re.I)

    for path in walk(".md", historical=False):
        if os.path.abspath(path) == os.path.abspath(policy):
            continue
        for lineno, line in enumerate(strip_fences(open(path).read()).split("\n"), 1):
            if not context.search(line):
                continue
            for m in restated.finditer(line):
                num, qualifiers = m.group(1).lower(), m.group(2).lower()
                # Describing the rule this policy replaced is not drift, and a
                # tracking note about fixing a stale restatement elsewhere has
                # to be able to quote the stale wording.
                if re.search(r"\b(was|were|used to|earlier|before|first|old|superseded|"
                             r"replaced|former|legacy|deprecated|no longer)\b", line, re.I):
                    continue
                # Nor is naming a count that is explicitly not enough yet —
                # "only 2 independent episodes" is the rule working, not drift.
                if re.search(r"\b(only|not eligible|ineligible|insufficient|fewer|"
                             r"not yet|does not count|short of|no more than)\b", line, re.I):
                    continue
                if num != want:
                    fail("threshold",
                         f"{rel(path)}:{lineno}: says '{m.group(0).strip()}' but the "
                         f"policy says {want} — one of them is wrong")
                elif "independent" not in qualifiers:
                    fail("threshold",
                         f"{rel(path)}:{lineno}: '{m.group(0).strip()}' drops "
                         f"'independent'; without it, one event summarised twice counts twice")


def check_orphans():
    """A doc nothing links to cannot be found, and cannot be corrected when the
    file that contradicts it changes. Anything under docs/ or examples/ must be
    reachable from at least one other file."""
    linked = set()
    for path in walk(".md"):
        base = os.path.dirname(path)
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", strip_fences(open(path).read())):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(base, target))
            if resolved != os.path.abspath(path):
                linked.add(resolved)
    for path in walk(".md", historical=False):
        if rel(path).split(os.sep)[0] not in ("docs", "examples"):
            continue
        if os.path.abspath(path) not in linked:
            fail("orphans", f"{rel(path)} is linked from nowhere — no reader will find it")


def check_shell():
    for path in walk(".sh"):
        r = subprocess.run(["bash", "-n", path], capture_output=True, text=True)
        if r.returncode:
            fail("shell", f"{rel(path)}: {r.stderr.strip().splitlines()[0]}")


def check_privacy():
    for path in walk(".md", ".yml", ".yaml", ".sh", historical=False):
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

    _, disabled = load_allowlist()
    check_frontmatter(cmds)
    check_commands(cmds)
    check_links()
    check_templates(cmds)
    check_counts(cmds)
    check_threshold()
    check_orphans()
    check_shell()
    if "privacy" in disabled:
        notes.append(f"privacy check disabled — {disabled['privacy']}")
    else:
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
