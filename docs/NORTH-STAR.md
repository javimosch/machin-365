# North star: first task saved, no terminal needed

> **Someone new goes from one install command to their first saved task without
> typing another command.**

This is a direction, not a promise. **Today we do not meet it.** See
[VISION.md](VISION.md) for why it matters and [ROADMAP.md](ROADMAP.md) for the
order of work.

The one install command is the exception for now. A non-technical person should
not need it either, and removing it is a later goal.

## The one number

**Extra terminal commands between installing and the first saved task.** The
target is **0**.

It is read with a pass condition: the task is still there after closing and
reopening the app. A run that loses it fails, whatever the count.

## Two guards

| Guard | Target |
|---|---|
| Known ways to lose or silently overwrite data | none open |
| Released programs that fail to run on a system we say we support | none |

**Supported systems:** Ubuntu 22.04 and 24.04, x86-64. We publish ARM64 builds
but have not run them, so we don't claim them yet.

## Where it stands (checked 2026-11-28)

| Check | Today |
|---|---|
| Extra commands | ❌ more than 0. Storage and apps are set up with `machin-365` commands, and the launcher is not released yet |
| Task still there after reopening | ⬜ not measured from a clean install |
| Data safety | ❌ copies with the same timestamp can stay different without any warning ([#37](https://github.com/javimosch/machin-365/issues/37)) |
| Ubuntu 22.04 | 🟡 Tasks 0.2.2 opened and showed stored tasks; Chat 0.2.3 showed incoming messages. The whole first-use path has not been run |
| Ubuntu 24.04 | 🟡 Tasks 0.2.2 and Chat 0.2.3 pass startup checks with a virtual display; the whole first-use path has not been run |

## How to measure it

On a clean Ubuntu 22.04 and a clean 24.04 desktop, with only the released
files:

1. Run the one install command.
2. Using only windows, menus and buttons, reach Tasks and add a task.
3. Close Tasks, open it again and look for the task.

Record each extra command, each place where a person would be stuck, and the
result of step 3. Publish the result, including a bad one.

A count of zero shows that it **can** be done without a terminal. It does not
show that a person **understands** what to do. Once the count is zero, watch a
non-technical person try it, without helping them, and write down where they
stop.

## Why not usage numbers

The anonymous usage counts carry no installation identifier, so they cannot
tell whether the same person came back. We will not add one to get a metric.
