# Roadmap

Ordered by what most threatens the [north star](NORTH-STAR.md). The order is a
proposal and there are no dates. Checked 2026-11-28.

**Reproduced** means it was observed. **From reading** means the code suggests
it and nobody has reproduced it: reproduce it first, and drop it if you can't.
**Missing** means it is not built.

## Now: it must run, and keep your data

Done: the suite and storage server no longer crash on 22.04 when looking up a
server name (people on suite 0.4.0 there have to rerun the install script,
because its `update` crashes too), and Tasks and Chat 0.2.2 start on 22.04 and
24.04.

| Item | Evidence |
|---|---|
| The chat message list stays on the oldest messages when many arrive | reproduced |
| Chat release builds are not yet checked for the room and name they join with ([machin-chat#11](https://github.com/javimosch/machin-chat/pull/11)) | missing |
| Copies with equal timestamps and different content are reported as the same ([#37](https://github.com/javimosch/machin-365/issues/37)). The open fix ([#63](https://github.com/javimosch/machin-365/pull/63)) picks a winner by content hash, so an older copy could overwrite a newer edit. Compare each copy with the last synced one instead, and keep both or report a conflict when both changed | difference: reported in #37; overwrite risk: from reading |
| A refused collection is reported as a typo and sync exits successfully ([#168](https://github.com/javimosch/machin-365/issues/168), fix proposed in [#170](https://github.com/javimosch/machin-365/pull/170)) | reported in #168 |

## Next: no terminal

| Item | Evidence |
|---|---|
| Release the launcher, so it does not have to be built from source, and have the install command add it | missing |
| Set up storage from the launcher | missing |
| Run the [north star measurement](NORTH-STAR.md#how-to-measure-it) on both supported systems | missing |

## Then: it should feel right

| Item | Evidence |
|---|---|
| Changing section in the launcher can take up to about a second. The desktop toolkit draws no new frame after handling input ([machin-desktop#1](https://github.com/javimosch/machin-desktop/issues/1)). One extra frame brought the typical delay from about 490 ms to 9 ms in a trial copy | reproduced |
| Choosing an app that is already open does not bring its window forward | from reading |
| Menu entries pass the suite folder and port in a key the desktop file format does not allow, so a custom setup may open with the default one | from reading |
| Show whose data is open, also after signing out. Signing out clears the tokens and does not switch the local data | from reading |

## Later: pulled by real use

- Sign-in and sync controls in the launcher, with a result that says whether the
  last sync worked.
- An install that needs no terminal at all.
- A chat server a non-technical person can use.
- Optional profiles, if someone needs them ([accounts](VISION.md#accounts)).
- Other languages, more apps, other platforms.

What we have decided not to build is in [VISION.md](VISION.md#not-the-goal).
