# Sheets: brief

**Status: proposal.** The mockup is approved (light by default, 2026-11-28); the user, tasks and scope below are not yet confirmed. [DOR.md](DOR.md) says what
is still missing before building starts. [Mockup](mockup.html)
([live](https://hart.intrane.fr/a/machin-365/sheets-mockup)).

## Who it is for (assumed)

Someone in a small organisation (an association, a small office) who keeps
budgets and lists. They are not technical. They receive files from other
people and send files back.

## The tasks (assumed)

1. Start a new sheet, type a list, save it, and find it again the next day.
2. Keep a monthly budget with amounts in euros and a total that updates.
3. Open an Excel file someone sent, change a few cells, and send it back
   without losing anything they would notice.
4. Open a CSV export (a bank, a form tool) without its codes, phone numbers
   or dates being changed.
5. Sort a list by a column without breaking its rows apart.
6. Find a name or an amount in a long list.
7. Copy a block of cells to and from other programs.
8. Fix a mistake with Undo, including after pasting or sorting.
9. Close the app, or lose power, without losing work they thought was safe.

## First version

- One sheet per file, up to 20,000 rows and 26 columns.
- Text, numbers, dates, money. Bold. Column widths.
- Formulas: `+ - * /`, brackets, cell references and ranges, `SUM`,
  `AVERAGE`, `MIN`, `MAX`, `COUNT`, `ROUND`, `IF`. References adjust when
  cells are copied.
- Open and save `.xlsx` (**assumed** to matter most) and CSV.
- Undo and redo, sort, find, copy and paste.
- Safe save, recovery of unsaved work, and a warning before closing.

## Not in the first version

Charts, pivot tables, several sheets in one file, merged cells, macros,
images, comments, conditional formatting, printing and PDF export, sync,
shared editing, `.ods`.

A file containing something Sheets cannot keep says so **before** it can be
overwritten.

## Rules for saving a changed .xlsx (from testing)

- Change only the edited cells; leave the rest of the file as it was.
- **Never leave a stored formula result that may be out of date.** LibreOffice
  shows stored results as they are. Until Sheets computes every formula in a
  file itself, remove all stored results when saving a change. The cost: a
  viewer that does not calculate (a file preview, for example) shows those
  cells empty (**not tried**).
- A save runs inside `arena { }`, so that repeating it does not grow memory.
- Sheets must calculate formulas itself to show them. What it shows for a
  function it does not support is **still to be decided**.

## Speed targets

Measured on the released build with the largest sheet above, on an 8-thread
laptop.

| What | Target | How it is measured |
|---|---|---|
| Open a 20,000-row file | under 2 s | time from launch to first full frame |
| Recalculate 20,000 formulas | under 100 ms | timed in a headless test |
| CPU time per frame while scrolling | under 8 ms | the toolkit's `--bench` |
| Key press or click to updated screen | median under 50 ms | simulated input, watching pixels |
| Memory | under 300 MB | resident size after open and 5 minutes of use. **To decide:** a separate limit for the peak while saving (the trial reaches about 400 MB) |
| Forced close | the saved file is never damaged; at most 30 s of typing lost | kill the app repeatedly |
