# Sheets: Definition of Ready

**Not ready.** No app code yet. Rules: [app-delivery](../../../.agents/skills/app-delivery/SKILL.md).
State on 2026-11-28.

| Ready? | Requirement | State and evidence |
|---|---|---|
| ⬜ | Kind of user and 5–10 tasks | Written in the [brief](BRIEF.md), **assumed**. The owner has not confirmed them |
| ⬜ | Sample files and rules | Three CSV [samples](samples/README.md) and proposed rules. No `.xlsx` samples yet |
| ⬜ | Mockups approved | [Mockup](mockup.html) with 9 screens, **waiting for approval** |
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
| Show and store decimal numbers | **Blocked in machin:** `str()` and `json()` keep 6 digits ([machin#774](https://github.com/javimosch/machin/issues/774)). Needs the fix, or Sheets' own number formatting and no `json()` for values. Binary floating point for money also needs a decision |
| Read `.xlsx` | **Blocked in machin:** zip entries cannot be unpacked ([machin#775](https://github.com/javimosch/machin/issues/775)). Needs a builtin, a C shim or an MFL inflate. XML reading and writing `.xlsx` **not tried** |
| Edit text in a cell | **Missing in the toolkit:** no text selection. Not tried |
| Choose a file to open or save | The toolkit has no file picker that I found. **Not tried** |
| Scroll sideways, resize columns | **Not tried** |
| Speed on a real screen | **Not tried** |

## Needed from the owner

1. Approve the mockup or say what to change; light or dark.
2. Confirm or correct the user and tasks.
3. Which files matter: Excel, LibreOffice, or both.
4. A few real files with private data removed (not committed without approval).
