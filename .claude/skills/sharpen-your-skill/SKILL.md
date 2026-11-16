---
name: sharpen-your-skill
description: >-
  Rewrites an existing skill so that a cheaper, smaller or faster model follows
  it reliably, without changing what the skill does. Use when the user says
  "sharpen this skill", "sharpen your skill" or "sharpen all my skills", asks
  to make a skill work on a cheaper model, says a smaller model ignores, skips
  or misreads a skill, or is handing skills over from a stronger model to a
  weaker one. Also use to tighten a vague or bloated SKILL.md. Do not use to
  write a new skill from nothing.
---

# Sharpen your skill

Rewrite one existing skill so that a cheaper model does the same job with it that a stronger model does. The skill's behavior stays the same. Only the clarity of the writing changes.

The work is finished when all four are true:

1. The sharpened skill is saved in the place step 1 names.
2. `check_preserved.py` prints `OK`, or every item it lists is in your report as removed on purpose.
3. A cheaper model has listed the right steps from the sharpened skill, or your report says the test was not run and why.
4. The user has the report from step 8.

## Why a skill fails on a cheaper model

A stronger model fills gaps. It infers an unstated order, picks a sensible meaning for "appropriate", and remembers a constraint from 200 lines earlier. A cheaper model differs in three ways, and each rewrite rule below answers one of them:

- It reads literally. A vague word gets an unpredictable reading.
- It loses instructions in long text. A rule that sits far from the place it applies gets skipped.
- It stops early, or reports success without checking, unless the skill says what finished looks like.

## Steps

Do the steps in order. Do not start a step until the one before it has passed.

### Step 1. Find the skill and decide where the result goes

Find the skill:

- The user gave a path: use that path.
- The user gave a name: look for `<name>/SKILL.md` in the project's `.claude/skills/` first, then in `~/.claude/skills/`.
- The user said "all" or "every": list each `SKILL.md` under the project's `.claude/skills/`. Sharpen one skill at a time. Finish steps 2 to 7 for one skill before you start the next. Skip `sharpen-your-skill` itself unless the user names it. Give one combined report at the end.
- No match, or more than one match: ask the user which skill they mean. Do not guess.

Decide where the result goes by looking at the skill's path:

| The path contains | Where to write the sharpened skill |
| --- | --- |
| `/skills/synced/` or `/plugins/` | A new folder, `<work dir>/sharpened/<name>/`. These folders are managed copies, and a later sync overwrites any edit made in them. Leave the original untouched. |
| anything else | The same folder as the original. |

`<work dir>` is your scratchpad directory if you have one. Otherwise create one with `mktemp -d`.

### Step 2. Back up the original

Run `cp -r <skill dir> <work dir>/<name>.orig`.

Pass: `<work dir>/<name>.orig/SKILL.md` exists. Step 6 compares against this copy, so do not edit it.

### Step 3. Read everything and write the inventory

Read `SKILL.md` from first line to last, and every file it points to. Then write `<work dir>/<name>.inventory.md` with these seven lists:

1. **Purpose.** One sentence: what the skill produces.
2. **Trigger.** When the skill is meant to load.
3. **Steps.** Every action the skill asks for, in order.
4. **Constraints.** Every "must", "must not", confirmation and warning.
5. **Payload.** Every command, path, file name, template, number and URL.
6. **Judgment calls.** Every place the skill leaves a choice to the reader.
7. **Unclear.** Every sentence that has two possible readings.

The inventory is what you check the rewrite against. Without it you cannot tell what the rewrite lost.

### Step 4. Rewrite the body

Apply rules R1 to R12 from "Rewrite rules" below. Stay inside "What must not change".

### Step 5. Rewrite the description

The `description` in the frontmatter decides whether the skill loads at all, and a cheaper model loads skills less often than it should. Write it so that it has, in this order:

1. What the skill does, in third person. Example: "Builds release notes from merged pull requests."
2. When to use it, with the words a user would type, in quotes.
3. When not to use it, if another skill covers a nearby task.

Keep it under 1024 characters. Put every "when to use" statement here and none in the body, because the body is not read until after the skill has loaded.

### Step 6. Check that nothing was lost

1. Run `python3 <this skill's base directory>/scripts/check_preserved.py <work dir>/<name>.orig <folder of the sharpened skill>`.
2. Pass: the output starts with `OK`.
3. If the output starts with `MISSING`, handle each listed item. Put it back character for character, or, if you removed it on purpose, add it to the "Removed" part of the report with the reason. Then run the script again.
4. Open the inventory. For each entry in lists 3 and 4, find the sentence in the sharpened skill that carries it. If you cannot find one, add it.
5. Read the frontmatter. It must start with `---`, keep the original `name`, and have a `description`.

### Step 7. Test on a cheaper model

Pick the model:

- The user named a model: use it.
- Otherwise: use the smallest current model whose ID you know. Your system prompt may list model IDs.
- You know no ID, or `which claude` prints nothing: skip this step and write "Not tested on a cheaper model" with the reason in the report.

Then:

1. Write one request that a real user of this skill would type.
2. Run this, with the three placeholders filled in:

   ```bash
   timeout 180 claude -p 'Read <path to sharpened SKILL.md> and treat it as your instructions. Do not change any file. Do not run any command that changes anything. List the exact steps you would take, in order, with the exact commands, for this request: <request>' --model <cheaper model>
   ```

3. Compare the answer with inventory lists 3, 4 and 5. Is every step there, in the right order? Is every constraint kept? Is every command and path exact?
4. Sort each miss into one of two kinds:
   - The original skill covers the point, and your rewrite did not carry it clearly. Find the sentence in the sharpened skill that should have produced the right answer, and rewrite it with the rule it breaks.
   - The original skill never covers the point. Do not add it. List it under "Gaps found" in the report, so the user decides.
5. If you edited the sharpened skill in point 4, run step 6 point 1 again, then run the test command again. The last test run must be on the final text.
6. Stop after two reruns. List any miss that remains in the report.

The test asks for a description of the steps, and forbids changes, so that a skill which deploys, sends or deletes is safe to test.

### Step 8. Report

Reply with this template, filled in:

```
Sharpened: <name>
Saved to: <path>
Backup: <work dir>/<name>.orig
Changes: <3 to 6 lines, each naming a rule (R1 to R12) and what it changed>
Assumptions: <each rule or number you supplied yourself, or "none">
Gaps found: <each point the original never covers, which you did not add, or "none">
Removed: <each item removed on purpose, with the reason, or "none">
Preservation check: <the first line of the script's output>
Cheaper-model test: <model, request, result of the last run; or "Not tested" and the reason>
```

Add text after the template in one case only. If the result went to `<work dir>/sharpened/<name>/`, add one line: the original is a managed copy, so the user must replace it at its source. For a claude.ai account skill, that means uploading the sharpened folder as a ZIP on claude.ai. In every other case the reply ends with the template.

## Rewrite rules

**R1. Start with the purpose and the finish line.** The first lines of the body say what the skill produces. Then comes a short list of conditions that are true when the work is finished. A cheaper model that does not know the end state stops too early or keeps going.

**R2. Write a sequence as numbered steps.** One action per step. For each step that can go wrong, add the check and what a pass looks like.

- Before: `Make sure the migration is safe, then apply it.`
- After: `1. Run npm run migrate:dry. Pass: the last line is "0 errors".` then `2. If step 1 passed, run npm run migrate. If it did not, stop and report the first error line.`

**R3. Replace a judgment word with a decision rule.** Search the skill for these words: appropriate, as needed, if necessary, relevant, reasonable, properly, good, clean, consider, try to, where possible, usually, etc. For each one, write the condition a reader can observe and the default to use when unsure. Take the rule from the rest of the skill or from its examples. If the skill gives no basis, supply the smallest rule that removes the vagueness, based on what a careful expert would do by default, and list it under "Assumptions" in the report. The rule may decide how an existing action is done. It may not add a new action. If the word adds nothing, delete it.

- Before: `Use an appropriate chart for the data.`
- After: `Change over time: line chart. Comparison between categories: bar chart. Anything else, or when unsure: a table.`

**R4. Give the literal payload.** Write the exact command, path, file name and output template in place of a description of it. If the original does not give the exact command, do not invent one. Write how to find it, for example "read the `scripts` section of `package.json`". An output format becomes a template in a code block.

**R5. Say what to do on failure and when to stop.** Every step that can fail gets a retry limit, a stop condition, and what to report. Say when to ask the user.

- Before: `Retry if the upload fails.`
- After: `If the upload fails, wait 10 seconds and try once more. If it fails again, stop and report the error text.`

**R6. Replace shouting with a plain rule and its reason.** Remove capitals, exclamation marks and words such as CRITICAL. State the rule once, then the reason, then what to do instead. Emphasis makes a cheaper model apply a rule too widely. A reason shows where the rule ends. Use a reason the original gives or implies, and do not invent a fact.

- Before: `NEVER EVER edit generated files!!!`
- After: `Do not edit files under gen/. The build overwrites them, so the edit is lost. Change the template in templates/ instead.`

**R7. Use one name for each thing.** Pick one term and use it every time. Define it where it first appears. Where "it" or "this" could point at two things, write the noun.

**R8. Settle conflicts.** Where two rules can collide, write which one wins.

**R9. Show a worked example.** Give one example of the main output, and one wrong-and-right pair for the most likely mistake. Label each as an example, so the model does not copy it word for word. Keep every example the original had.

**R10. Put the common path first and keep the file short.** Rare branches go after the main steps. Move reference material longer than 100 lines to `references/<topic>.md`, and leave a pointer of the form "Read `references/<topic>.md` when <condition>". Delete repeated rules and filler such as "be careful" and "think step by step". Keep the body under 300 lines.

**R11. End with a pre-finish checklist.** Add 3 to 7 yes-or-no questions that cover the constraints most costly to miss. A cheaper model loses early instructions during long work, and a checklist at the end brings them back.

**R12. Leave open what the original left open on purpose.** Some skills want variety, such as writing or design skills. Do not turn those choices into fixed steps. State the test for a good choice and leave the choice free.

## What must not change

- The `name`, and every frontmatter key other than `description`.
- Every command, path, file name, number, template and URL. Copy each one character for character.
- Every confirmation step and safety warning.
- Bundled scripts, assets and licence files. Do not edit or delete them.
- What the skill does. Do not add a new action. Use this test: can you point to the sentence in the original that asks for the action? If you can, the action stays and you may make it more exact. If you cannot, leave the action out and list it under "Gaps found" in the report. Example: the original says "list the merged PRs". Writing the exact command for that is allowed. Adding "then drop the PRs that users will not notice" is a new action, so it goes under "Gaps found".
- One exception: a check on an existing step is allowed, because R2 asks for it. List each check you supplied under "Assumptions".

If a sentence has two readings that lead to different behavior, choose the reading that fits the rest of the skill, write it out plainly, and list it under "Assumptions". If one of the readings would delete, send, publish, deploy or spend, ask the user before you choose.

## Before you report

Answer each question. Fix every "no" first.

1. Did the last run of `check_preserved.py` print `OK`, or is every `MISSING` item in the report?
2. Is the `name` in the frontmatter the same as in the backup?
3. Does every entry in inventory lists 3 and 4 have a sentence in the sharpened skill?
4. Can you point to a sentence in the original for every action in the sharpened skill?
5. Is every rule or number you supplied yourself listed under "Assumptions"?
6. Did you run step 7 on the final text, or does the report say "Not tested" with the reason?
7. Is the backup at `<work dir>/<name>.orig` still unedited?
