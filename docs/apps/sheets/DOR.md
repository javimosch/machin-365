# Sheets: Definition of Ready

**Not ready.** No app code yet. Rules: [app-delivery](../../../.agents/skills/app-delivery/SKILL.md).
State on 2026-11-28.

| Ready? | Requirement | State and evidence |
|---|---|---|
| ⬜ | Kind of user and 5–10 tasks | Written in the [brief](BRIEF.md), **assumed**. The owner has not confirmed them |
| ⬜ | Sample files and rules | Three CSV [samples](samples/README.md) and proposed rules. No `.xlsx` samples yet |
| ✅ | Mockups approved | [Mockup](mockup.html), 9 screens, **approved by the owner on 2026-11-28, light by default** |
| ✅ | What the first version will not do | [Brief](BRIEF.md#not-in-the-first-version) |
| ⬜ | Toolkit features tried | See below: some tried, some not |
| ✅ | Speed targets and how to measure | [Brief](BRIEF.md#speed-targets), proposed numbers |

## Spikes

Throwaway code is in [spikes/](spikes/). Measurements are from Ubuntu 22.04,
x86-64, machin 0.142.0, on a virtual display (CPU time only; no real GPU).

| Question | Result |
|---|---|
| Can the toolkit draw a big grid? | **Yes.** 100,000 × 26, drawing only visible cells: 2.6 ms CPU per frame over 600 frames |
| Select ranges by mouse and keyboard | **Yes.** Drag, arrows, Shift+arrows, Page Down, with simulated input |
| Copy and paste blocks | Tab-separated text round trip **within the app**. Other programs: **not tried** |
| Formula speed | 20,000 simple formulas plus a sum, parsed each time: 5.2 ms. The spike has no dependency order and few operators |
| Warn before closing | **Needs a toolkit change.** The toolkit quits on any close request. With a [patched copy](spikes/close-guard-host.patch) the app stayed open on SIGTERM and the unpatched one quit. The window's close button, and the two buttons in the warning, **not tried** |
| Safe save | Temp file, `fsync`, rename: 0 damaged files in 200 forced kills. Control (writing in place): damaged 4 times. Power loss **not tested**; the folder is not `fsync`ed |
| Show and store decimal numbers | Storing: fixed for `json()` in [machin#776](https://github.com/javimosch/machin/pull/776), merged, **not yet in a machin release**; `str()` still keeps 6 digits on purpose. Showing money and dates the way the user writes them is Sheets' own work and is **not tried**. Binary floating point for money still needs a decision |
| Unpack and repack `.xlsx` | **The zip layer works** with [machin#778](https://github.com/javimosch/machin/pull/778) (merged, **not yet in a machin release**). Four LibreOffice-made files, the largest 20,000 rows: every entry identical to Python's result, checksums good (16 MB in 45 ms, 27 MB peak). After rewriting in machin, LibreOffice showed a changed amount, and read the 20,000-row file the same as before. [Reader](spikes/unzip.src), [writer](spikes/rezip.src) |
| Read cell contents | **Works in the [spike](spikes/cells.src):** text (shared, inline, mixed formatting, line breaks, spaces, emoji), numbers, dates, booleans, formulas including shared ones. A LibreOffice-made file (27 cells) and a **hand-made** file in Excel's style (15 cells) match known values; 200,010 cells of a 20,000-row file match the source CSV. Machin's `xml.src` is too slow to use, so the spike has its own scanner |
| Change cells and save | **Works if stored formula results are removed.** Only edited cells change in the sheet XML; in LibreOffice, 26 other cells, styles, merged cells and a second sheet were unchanged. With results kept, 3 of 4 dependent totals and a text formula showed **old values**, even with `fullCalcOnLoad` set; with them removed, all were right. Editing the master of a shared formula kept the others correct |
| Memory, in a [window trial](spikes/trial/README.md) with editing and undo | 🟡 **Normal use is well under 300 MB; saving goes over it.** See [the trial](#window-trial) |
| Speed in the window trial | 20,000 × 26 on a virtual display: grid on screen about 0.6 s after launch (target 2 s); key press to changed screen, median 21–24 ms, worst 298 ms once (target: median 50 ms); 1.9 ms CPU per frame with a **still** grid (target 8 ms while scrolling, **not measured while scrolling**). A save **freezes the window for 0.6–0.7 s**; there is no target for that |
| Files from Microsoft Excel | **Not tried:** neither reading a real one nor opening a saved one in Excel. Also not handled: the 1904 date system, dates before March 1900, writing to other than the first sheet, inserting or deleting rows, the used-range record |
| Select and edit text in a field | Merged in [machin-desktop#3](https://github.com/javimosch/machin-desktop/pull/3): 24 unit tests; 15 scripted mouse and keyboard steps in a real window pass. Copy and paste with other programs, double-click word selection and editing **inside a grid cell**: not tried |
| Choose a file to open or save | The toolkit has no file picker that I found. **Not tried** |
| Scroll sideways, resize columns | **Not tried** |
| Speed on a real screen | **Not tried** |

## Window trial

Two files of 520,000 cells, five minutes each of scripted use: about 65 typed
values, 19 pastes of 2,020 cells, deletes, 16 undos, 8 redos, scrolling and
10 saves.

| | No formulas | 120,000 formulas |
|---|---|---|
| Resident after opening | 189 MB | 174 MB |
| Resident after 5 minutes | 195 MB | 179 MB |
| Highest, during a save | 391 MB | 413 MB |
| Cells compared in the final file | 13,692, 0 wrong | 13,691, 0 wrong |

The app's record of cursor, undo steps and changes was compared with the test
script's during the run, with no mismatch. Three deliberate mismatches were all
caught.

How the trial holds a file:

- The file's sheet XML and numbers-only cell records, **reused by every save**.
  Records are in `alloc()` memory: assigning any list other than text to a
  global from a frame copies it through JSON
  ([machin#783](https://github.com/javimosch/machin/issues/783)). Doing that,
  the first build peaked at 1,192 MB and stayed at 821 MB. The cost: this
  memory is outside the language's checks.
- Edits are kept on top of the file, which is never changed in memory. A save
  always writes the original file plus all edits.
- Text is made only for the cells on screen.

Found in the toolkit: its state store has **4,096 slots, and when full it
silently writes into the first one** (from reading `host/host.c`; not
reproduced). The trial keeps edits and undo out of it.

Not covered: formula calculation (after an edit, formula cells show the formula
text), longer sessions, much larger undo histories, a real screen and graphics
card, real Excel files, and pasting formulas (references are not adjusted).

## What keeps memory down

- Scanning allocates nothing: tag names and attributes are compared in place.
- A cell is stored as numbers that point into the sheet's XML.
- The output is built in one pass. Copying it once per edit caused the
  gigabytes. That pass needs edits in cell order, so the save sorts them: the
  first version silently dropped unsorted edits, and the checks caught it.
- Old formula results are removed in the same pass, not by a second scan.
- **A save must run inside `arena { }`.** Without it, resident size grew about
  224 MB with each save, to 4.7 GB after 20 (the saved files were identical).

Not tried: reusing the scan made at open for saving (to lower the peak),
reserving list capacity, or holding less per cell.

## Needed from the owner

1. Confirm or correct the user and tasks.
2. Which files matter: Excel, LibreOffice, or both.
3. A few real files with private data removed (not committed without approval).
