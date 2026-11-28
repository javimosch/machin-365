# Sheets 0.1.0: Definition of Done status

**Released 2026-11-28 as an early version, at the owner's request. It does not
meet the whole Definition of Done**, and several
[Definition of Ready](DOR.md) boxes were still open. Code:
[machin-sheets](https://github.com/javimosch/machin-sheets). From this release
on, its README is the record of what Sheets does.

| Done? | Requirement | State and evidence |
|:-:|---|---|
| ⬜ | Every user task works from installation to reopening the saved file, **without a terminal** | **Installing needs a terminal.** Sorting (task 5) is **not built**: the owner asked for stabilising only. New, save, reopen, totals, editing an `.xlsx`, CSV, find, copy and paste, undo and recovery pass in the window tests |
| ✅ | Undo, copy and paste, keyboard use, unsaved-changes warning | Window tests, including pasting to and from another program (`xclip`) and the window's close request. LibreOffice and browsers as the other program: not tried |
| ✅ | Forced close within the recovery limit, saved file never damaged | A killed window offers its unsaved changes back. The safe-save method damaged 0 files in 200 forced kills (spike). The released app was not put through that kill loop, and power loss is not tested |
| ⬜ | Sample files open correctly in LibreOffice; content the app cannot keep is reported first | Files made by the unit and window tests open in LibreOffice with the same values and totals. Warnings exist for other sheets, oversize sheets, charts, pivot tables, macros, pictures and merged cells. Saving back charts, pivot tables, macros or pictures is **not tested** (the warning says so) |
| ✅ | The released download passes on Ubuntu 22.04 and 24.04 | Release CI ran the window tests on both architectures on 22.04. The downloaded amd64 file passed them again (49 checks), opened 200 damaged files without a crash, and starts in clean 22.04 and 24.04 containers. The window tests were **not** run on 24.04; the arm64 download was only checksum-verified |
| ⬜ | Owner approves the design and a non-technical person completes the tasks | The mockup was approved. The finished app has **not** been reviewed by the owner, and **no** non-technical person has tried it |
| ⬜ | Help text, website and roadmap match | README, website and roadmap updated for 0.1.0. There is no help inside the app |

## Not tried

Microsoft Excel (reading its files or opening saved ones in it), files from
real users, speed on a real screen and while scrolling, and Linux
distributions other than Ubuntu.

## What testing found before release

The window and damaged-file tests failed before these were fixed:

- closing while typing in a saved sheet quit and lost the text;
- clicking another cell while typing put the text in the wrong cell;
- saving left the recovery file behind;
- column edges could not be dragged;
- Save as did not put the cursor in the name box;
- 7 of 150 damaged files crashed the app (memory corruption in the sheet
  reader).

Found on the way:
[machin#786](https://github.com/javimosch/machin/issues/786) (`return ";"`
fails to compile) and
[machin-desktop#6](https://github.com/javimosch/machin-desktop/issues/6)
(key presses lost when a frame is slow, fixed).
