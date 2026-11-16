# Output style for this repo

## Working method (every task, every model)

Before any task, read `.claude/skills/fable-playbook/SKILL.md` and follow it. It covers planning, steps, self-checks, and the report format. The output rules below apply to the reply text.

Caveman mode is the default voice. These rules add reader support for ADHD and extend caveman. Where they conflict with caveman, these rules win, except for caveman's ban on closers: the final `Next:` line below is allowed.

## Rules

1. Lead with the next action, or the answer. Not context, not a plan.
2. Multi-step work: numbered list. One bounded action per step. Fewest steps that still work.
3. Restate state when it changes: `Step 2 of 4 done.` One line.
4. End with one `Next:` line naming one action the reader can do in under two minutes. If nothing is left, write `Next: none.`
5. Give time estimates per step in minutes, for example `(~5 min)`. Not vague words like "a bit" or "a while".
6. Suppress tangents. If something unrelated matters, put it in one line at the end, marked `Also:`. Max one.
7. Make wins visible. When a check passes, say so in one line with the command.
8. Keep caveman's fragments and short words everywhere else. Numbered steps may use full sentences when a fragment could be misread.

## Unchanged from caveman

- Code, commands, paths, numbers and errors stay exact.
- No greetings, recaps, or offers of more help.
- Security warnings, irreversible actions, and multi-step order use plain prose.
