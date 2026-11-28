# Sheets window trial (throwaway)

A grid with editing, cut, copy, paste, clear, undo, redo, bold, number, euro and
date formats, a total, find, a right-click menu and save, over the cell spike.
**Not the app**: no formula engine, one sheet, no warning before closing, no
file picker (so no New or Open), no sort.

The app is the source files here (`app.src`, `engine.src`, `styles.src`, `app.conf`),
built with `mdk build <folder>` using a machin build that includes
[#776](https://github.com/javimosch/machin/pull/776) and
[#778](https://github.com/javimosch/machin/pull/778). It reads the file named
by `IN` and writes `OUT`. The test scripts are kept as run; their paths are
the ones of the machine that ran them.

`test-harness.py` drives the app with real X input and keeps its own record of
what should have changed; saved files are read back with Python's zip and XML
libraries.
