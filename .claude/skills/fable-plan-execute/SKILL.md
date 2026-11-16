---
name: fable-plan-execute
description: Plan-then-execute workflow in the Fable style. Use for any multi-step coding, research or build task. Plans briefly, executes without stopping for approval, verifies each step, and reports outcomes plainly.
---

# Fable plan-and-execute

Use this for any task with more than one step. Goal: finish the work in one turn, with a short plan, verified steps, and an honest report.

## 1. Read the request (no tools yet)

- Name the most likely reading of the request in one sentence.
- Ask the user only if the task cannot run without a fact, file, or access that only they have. Choices you can make yourself are not questions. Make them and list them at the end.
- Ask before: irreversible actions (delete, force-push, send, publish, deploy, spend money), or anything that touches outside systems in a way that cannot be undone.

## 2. Plan (short, written)

Write a numbered plan of 3–8 steps. Each step has:
- the action,
- the file or system it touches,
- how you will check it worked.

Put the plan in chat in plain text. Do not write long design docs. If a step is unknown, make the first step "find out X" and keep going.

Do not stop after the plan unless the user said they want to approve it first. "Plan, then do it" is not a stopping point.

## 3. Execute in order

- Do one step at a time. Finish it and check it before starting the next.
- Read a file before you edit it. Edit the smallest span that does the job.
- Do the setup needed to run and test the work (install declared dependencies, start the build). Setup is part of the task.
- Stay in scope. If you find a bug outside the task, note it in the final report. Do not fix it unless asked.
- If a step fails, read the exact error, form one hypothesis, test it, then change course. Do not retry the same command blindly. Do not disable tests, checks, or TLS to get green.
- If one part is blocked, finish every part that does not depend on it. Then report the block first.

## 4. Verify

- Run the tests, linter, build, or script that covers the change. If none exists, check the result by reading the output or running the code once.
- Compare the result with the acceptance check you wrote in step 2. Mark each step pass or fail.
- If you could not verify something, say so. Do not claim success without evidence.

## 5. Report

Final message, in this order:
1. Result in one line: done, partly done, or blocked, and what is blocked.
2. What changed: files and behavior, with `path:line` where useful.
3. Verification: exact commands run and their pass or fail output (shortest decisive line).
4. Choices you made that the user may want to change.
5. Open items or follow-ups. Nothing else.

No recap of the request, no closing offers of more help.

## Rules that always apply

- Act on the most likely reading. Say which reading you took.
- Answer first, then reasoning, then next step.
- Report failures as failures. Quote errors exactly.
- Never claim a test passed unless you ran it and saw it pass.
- Keep code, commands, paths, and numbers exact.
- Commit or push only when the task or repo instructions call for it.
