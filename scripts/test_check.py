#!/usr/bin/env python3
"""Tests for scripts/check.py.

check.py is the only thing in this repo that executes. Everything else is
prose, which means check.py is the sole enforcement point for every invariant
the system relies on — and if one of its regexes quietly stops matching, it
prints "All checks passed" and enforces nothing. That failure is silent and
looks exactly like success, which is the same shape as the broken wiring
contracts /calibrate exists to catch.

So each check gets a test that injects the defect it was written for into a
throwaway copy of the repo and asserts it fires. Each test also asserts that
*no other* check fires, because an over-broad check is as bad as a missing
one: the threshold check's first real run flagged a sample that was correctly
demonstrating an insufficient count, and only exclusivity would have caught it.

Stdlib only.  python3 scripts/test_check.py   (or: python3 -m unittest discover scripts)
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Copied into each scratch repo. Anything not here is irrelevant to check.py,
# and leaving it out keeps the copy cheap enough to do per-test.
COPY = ("scripts", ".claude", ".github", "docs", "examples", "automation",
        "README.md", "INSTALL.md",
        # Linked from the README, so the links check needs them present.
        "LICENSE", ".gitignore")


def run(repo):
    """Run check.py against a repo. Returns (exit code, set of failed checks)."""
    proc = subprocess.run([sys.executable, os.path.join(repo, "scripts", "check.py")],
                          capture_output=True, text=True)
    # Failures print as "  <check>:" followed by indented "    - message" lines.
    failed = set(re.findall(r"^  ([a-z]+):$", proc.stdout, re.M))
    return proc.returncode, failed, proc.stdout


class CheckTest(unittest.TestCase):

    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="ll-check-")
        for name in COPY:
            src = os.path.join(ROOT, name)
            if not os.path.exists(src):
                continue
            dst = os.path.join(self.repo, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)

    # -------------------------------------------------------------- helpers

    def path(self, *parts):
        return os.path.join(self.repo, *parts)

    def append(self, rel, text):
        with open(self.path(rel), "a") as fh:
            fh.write(text)

    def sub(self, rel, old, new):
        p = self.path(rel)
        with open(p) as fh:
            text = fh.read()
        self.assertIn(old, text, f"fixture drift: {old!r} no longer in {rel}")
        with open(p, "w") as fh:
            fh.write(text.replace(old, new, 1))

    def write(self, rel, text):
        with open(self.path(rel), "w") as fh:
            fh.write(text)

    def assert_only(self, check):
        """The named check failed, and nothing else did."""
        code, failed, out = run(self.repo)
        self.assertEqual(code, 1, f"expected failure, got clean run:\n{out}")
        self.assertEqual(failed, {check}, f"expected only {check!r}:\n{out}")

    # ---------------------------------------------------------------- tests

    def test_clean_repo_passes(self):
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_frontmatter_unquoted_yaml(self):
        # `[` opens a flow sequence and takes the rest of the block with it.
        # Unquoting the real key rather than adding one: a second copy would be
        # overwritten by the first, which is its own defect (tested below).
        self.sub(".claude/commands/exam.md",
                 'argument-hint: "[topic] | apply [topic] [product]"',
                 'argument-hint: [topic] | apply [topic] [product]')
        self.assert_only("frontmatter")

    def test_frontmatter_duplicate_key(self):
        # Last one wins in every YAML parser, so a stale line above a corrected
        # one is invisible until something reorders the block.
        self.sub(".claude/commands/exam.md", "description:",
                 "description: an older description that no longer applies\ndescription:")
        self.assert_only("frontmatter")

    def test_command_reference_with_no_file(self):
        self.append("docs/skill-map.md", "\nRoutes onward to `/does-not-exist`.\n")
        self.assert_only("commands")

    def test_broken_relative_link(self):
        self.append("docs/skill-map.md", "\nSee [the missing one](no-such-file.md).\n")
        self.assert_only("links")

    def test_template_seeding_a_title_no_skill_matches(self):
        self.sub(".github/ISSUE_TEMPLATE/brainstorm.yml", "title:", "title: Sheldon: \n_old:")
        self.assert_only("templates")

    def test_readme_command_count_drifts(self):
        self.sub("README.md", "Ten slash commands", "Twelve slash commands")
        self.assert_only("counts")

    def test_readme_script_count_drifts(self):
        self.sub("README.md", "five shell scripts", "four shell scripts")
        self.assert_only("counts")

    def test_install_skill_count_drifts(self):
        self.sub("INSTALL.md", "of the ten skills reference the repo",
                 "of the twelve skills reference the repo")
        self.assert_only("counts")

    def test_threshold_restatement_drops_independent(self):
        # The bug that shipped: "three or more sessions" is the same number and
        # a materially weaker rule, because one event summarised twice counts twice.
        self.append("docs/skill-map.md",
                    "\nA pattern is promoted to memory after three or more sessions.\n")
        self.assert_only("threshold")

    def test_threshold_restatement_uses_wrong_number(self):
        self.append("docs/skill-map.md",
                    "\nA memory candidate needs four independent episodes.\n")
        self.assert_only("threshold")

    def test_threshold_allows_a_count_named_as_insufficient(self):
        # "only 2 independent episodes" is the rule working, not drift. This is
        # a real false positive the check produced on its first run.
        self.append("docs/skill-map.md",
                    "\nNot eligible for memory: only 2 independent episodes so far.\n")
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_threshold_allows_describing_the_superseded_rule(self):
        self.append("docs/skill-map.md",
                    "\nThe old rule promoted a memory after three sessions.\n")
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_threshold_allows_a_tracking_note_quoting_stale_wording(self):
        # A review item about fixing a stale restatement has to be able to
        # quote it. Found in the private workspace on the checker's first run.
        self.append("docs/skill-map.md",
                    '\n- [ ] The post still describes the superseded model '
                    '("three or more sessions" -> promoted) and needs redrafting.\n')
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_threshold_ignores_an_activity_count_that_is_not_a_rule(self):
        # "220 sessions logged as issues" shares a sentence with "memory
        # records" and is not a threshold. Also found on that first run.
        self.append("docs/skill-map.md",
                    "\nAs of August: 11 weekly reviews, 220 sessions logged as "
                    "issues, 40 memory records.\n")
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_policy_losing_its_canonical_rule_is_itself_a_failure(self):
        # Nothing can be checked against a policy that stopped stating the rule.
        self.sub("docs/memory-policy.md", "three **independent** episodes",
                 "several independent episodes")
        self.assert_only("threshold")

    def test_orphan_doc(self):
        self.write("docs/stray.md", "# Stray\n\nNothing links here.\n")
        self.assert_only("orphans")

    def test_broken_shell_script(self):
        # Unterminated `if` — a real parse error, not just a command that would
        # fail at runtime. `bash -n` only catches the former.
        self.append("automation/watcher.sh", "\nif true; then\n  echo unterminated\n")
        self.assert_only("shell")

    def test_privacy_leak_in_an_instruction_file(self):
        self.append("docs/skill-map.md", "\nQuestions to someone@somewhere.org.\n")
        self.assert_only("privacy")

    # ------------------------------------------------------------ allowlist

    def test_allowlist_silences_a_missing_command(self):
        self.append("docs/skill-map.md", "\nRoutes onward to `/does-not-exist`.\n")
        self.write("scripts/check-allow.txt",
                   "/does-not-exist  retired, still named in planning docs\n")
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)

    def test_allowlist_can_disable_the_privacy_check(self):
        self.append("docs/skill-map.md", "\nQuestions to someone@somewhere.org.\n")
        self.write("scripts/check-allow.txt", "!privacy  this workspace is private\n")
        code, failed, out = run(self.repo)
        self.assertEqual((code, failed), (0, set()), out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
