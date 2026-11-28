---
name: app-delivery
description: How a Machin 365 app goes from idea to release — the Definition of Ready (DoR) and Definition of Done (DoD). Use before starting, building, reviewing or releasing any Machin 365 app or a major feature of one (Sheets, Write, Slides, the launcher).
---

# Delivering a Machin 365 app

Agreed 2026-11-28. Audience: **non-technical people**
([vision](../../../docs/VISION.md)). Tasks and Chat were spikes. Real apps
replace office software **for a defined set of everyday jobs**, not feature for
feature.

## Rules

- **One app at a time**, end to end, before the next one starts.
- **Real files.** People open, save and send documents. Local files first,
  with reliable recovery. No document sync until record sync can handle
  conflicts without losing data.
- **The toolkit is part of the work.** A gap in
  [machin-desktop](https://github.com/javimosch/machin-desktop) is fixed there,
  not worked around in the app. Gaps in machin go to its issue tracker.
- Each app lives under `docs/apps/<app>/`: `BRIEF.md`, `DOR.md`, samples.

## Order of work

1. Brief: user and tasks.
2. Mockups, approved by the owner.
3. Spikes on whatever could make the app impossible.
4. One small workflow, complete from install to reopening the saved file.
5. Widen it, one user task at a time.
6. Release, then check the released download.

## Definition of Ready

No app code (spikes excepted) until every line is true. Record the state and
the evidence for each in `docs/apps/<app>/DOR.md`.

- [ ] A named kind of user and 5–10 real tasks they must complete.
- [ ] Sample files, with written rules for what must survive open and save.
      No private data in the repository.
- [ ] Mockups approved by the owner, including empty and error states.
- [ ] A written list of what the first version will not do.
- [ ] Each required toolkit feature tried in a small spike, with the result.
- [ ] Speed targets with numbers, and how they are measured.

An assumption does not tick a box. If the owner has not answered, write the
assumption down, mark it **assumed**, and leave the box open.

## Definition of Done

- [ ] Every user task works from installation to reopening the saved file,
      **without a terminal**.
- [ ] Undo, copy and paste, keyboard use and an unsaved-changes warning work.
- [ ] Forced-close tests meet the agreed recovery limit and never damage the
      last saved file.
- [ ] Sample files saved by the app open correctly in LibreOffice. Content the
      app cannot keep is reported **before** it can be lost.
- [ ] The **released download** passes its tests on Ubuntu 22.04 and 24.04.
- [ ] The owner approves the design, and a non-technical person completes the
      tasks without help.
- [ ] Help text, website and roadmap match what is released.

## What counts as evidence

Learned on this project; each cost a wrong release or a wrong report.

- **A check must be seen failing** on a broken build before its pass means
  anything. A bare container passed a binary that crashed on real desktops.
- **Starting is not working.** Chat 0.2.2 started, said "online" and sat in
  the wrong room. Test what the user does, and check what the app sends.
- **Test the released file**, not only a local build.
- **Suspect the harness** before reporting a crash: a fresh virtual display for
  each run, and check the app is alive *before* tearing anything down.
- **Diagnose before publishing.** Do not put a cause on the website or roadmap
  until a test separates it from the other explanations.
- Say what was not run (architecture, system, flow).

## Release

Merging, tagging and publishing need the owner's approval each time.
