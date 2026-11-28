# Sheets sample files

All names and figures are invented.

| File | What it exercises |
|---|---|
| `budget-comma.csv` | comma separator, point decimals, ISO dates, a quoted comma, a negative and a large amount |
| `budget-semicolon.csv` | semicolon separator, comma decimals, day/month/year dates |
| `contacts-tricky.csv` | byte-order mark, CRLF lines, leading zeros, `1E5` as a code, a cell starting with `=`, a line break inside a cell, quotes, outer spaces |

## Rules for opening and saving (proposed)

- A value the user did not edit is written back as it was read.
- Text that looks like a number or date but is a code stays text: `00042`,
  `1E5`, `0612345678`.
- **Nothing in a CSV is run as a formula.**
- The separator, decimal mark and date order are shown before opening and can
  be changed.
- Saving a CSV keeps its separator, line endings and byte-order mark.

LibreOffice's default command-line CSV import, for comparison, turned `00042`
into `42` and `1E5` into `100000`, and ran `=not a formula` as a formula
(`Err:509`).

**Missing:** `.xlsx` samples, including a file with a chart and merged cells,
and real files from a user with private data removed.
