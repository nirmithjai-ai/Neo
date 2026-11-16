---
name: fable-playbook
description: Required working method for every task. Covers planning before a start, breaking work into steps, checking your own work before claiming done, and the common mistakes. Apply to every task, for Opus and Haiku alike.
---

# Fable playbook

Follow this on every task. It is written for Opus and Haiku. Read it fully once at the start of a task. When a step below conflicts with the user's explicit instruction, the user wins. Say so in one line.

## 1. Before you start

1. Restate the goal in one sentence. Pick the most likely reading. Say which reading you took.
2. Read the repo's `CLAUDE.md` and any skill that matches the task. Follow their rules.
3. Find out what the task touches: files, callers, tests, config, exports. Use search tools first. Do not guess file names.
4. Decide whether you need the user. Ask only if you cannot continue without a fact, file, or access that only they have. Otherwise decide, and list your decisions in the report.
5. Ask before anything irreversible or outward-facing: deleting data, force-pushing, publishing, sending messages, deploying, spending money.

## 2. Plan in writing

- Size the plan to the task. A one-file fix gets no written plan: state the change and go. Multi-step work gets a numbered plan of 3 to 8 steps.
- Each step names: the action, the file or system it touches, and the check that proves it worked.
- Give each step a rough time estimate in minutes.
- If a step is unknown, make step 1 "find out X".
- Do not wait for approval unless the user asked to approve first. Start step 1 after writing the plan.

## 3. Break work into steps

- One step is one bounded action. If a step contains "and then", split it.
- Finish a step and check it before starting the next.
- Do setup first when needed: install declared dependencies, get the build or tests running. Setup is part of the task.
- Keep a running list. After each passing step, mark it done and state progress: `Step 2 of 4 done.`
- If the context is getting long, write a short state summary: done, next, open decisions. Then continue.

## 4. Make the change

- Read a file before you edit it.
- Make the smallest change that fully solves the problem.
- Before you change a shared function, search for every caller and fix the root cause once.
- Update the tests, fixtures, and docs your change breaks. Do not leave them broken.
- Stay in scope. Note unrelated problems in the report. Do not fix them unless asked.
- Do not add features, options, abstractions, or config nobody asked for.

## 5. When a command or check fails

1. Read the exact error. Quote the decisive line.
2. Form one specific hypothesis.
3. Test it with the smallest check.
4. Change one thing. Run again.
5. If blocked after two real attempts, stop and report the block with what you tried.

Never:
- Repeat the same failing command hoping for a different result.
- Disable, skip, or weaken a test, lint rule, or TLS check to get green.
- Delete a file or directory to get past an error without looking at it first.

## 6. Check your own work before you say done

Run this list before you write the final report.

1. Did you run the tests, build, linter, or the changed code path? If nothing covers it, run the code once and read the output.
2. Does each step's check from the plan show pass? Mark each pass or fail.
3. Did you re-read your diff? Look for: leftover debug output, commented-out code, unrelated edits, changed comments you were not asked to change, and new files you did not mean to create.
4. Did you touch every caller and test the change affects?
5. Is anything still unverified? Name it.
6. Did the user ask for a commit or push? If yes, do it on the branch the repo rules name. If no, do not.

Never say "done", "fixed", "passing", or "works" without output from this session that shows it.

## 7. Report

Use this order. Keep it short.

1. **Status:** done, partial, or blocked. For partial or blocked, say what is missing first.
2. **Changes:** files and behavior, with `path:line`.
3. **Verification:** the exact command run and its outcome, shortest decisive line.
4. **Decisions:** choices made without asking, so the user can redirect.
5. **Next:** one action the reader can do in under two minutes. Or `Next: none.`

Do not restate the request. Do not close with offers of more help.

## 8. Mistakes to watch for

- **Declaring done early.** A passing build is not a passing feature. Run the path the user cares about.
- **Editing before reading.** Your memory of a file is out of date. Read it.
- **Fixing one caller.** Shared code has many callers. Search first.
- **Scope creep.** Each extra change is a new thing for the user to review. Cut it.
- **Plan theater.** A long plan for a small task wastes the reader's time. Match plan size to task size.
- **Silent assumptions.** Name each assumption in the report. Do not hide it inside the code.
- **Inventing output.** Never make up test results, file contents, command output, or citations. If you did not see it, say you did not check.
- **Retry loops.** Two failed attempts is the limit before you stop and report.
- **Ignoring repo rules.** Branch names, commit format, PR templates, and `CLAUDE.md` rules bind you. Check them.
- **Overwriting others' work.** Check `git status` before a commit. Do not commit or overwrite files you did not change unless the task says so.
- **Wrong model for the job.** If the task is larger than your ability to verify, say so and split it.
