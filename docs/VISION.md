# Vision

> This is the intent. The [README](../README.md) says what is built, and the
> [roadmap](ROADMAP.md) says what is missing.

**Everyday desktop apps in one place, for people who don't use a terminal.**
Your work is on your own computer. Sync is there if you want it.

## Who it is for

People who are not technical. They want to keep a to-do list or talk with
their team. They should not need to know what a server, a port, a token or a
terminal is.

Developers matter too, because Machin 365 is also how
[machin](https://github.com/javimosch/machin) gets tested by real use. When the
two disagree about what a screen should say or do, the non-technical person
wins.

## The shape

| Piece | Job |
|---|---|
| **Machin 365** (the launcher) | The one window: install apps, open them, see where your data is |
| **Apps** (Tasks, Chat) | Do one everyday job each |
| **Storage** (a local [machin-bkn](https://github.com/javimosch/machin-bkn)) | Keeps app data on your computer |
| **Sync** (optional) | Copies stored data to a server you choose, and back |
| **`machin-365`** (the command line) | Everything the launcher drives, for developers and automation |

## Principles

1. **No account to use your own computer.** An account is for things that
   involve other devices or people, such as sync.
2. **Plain words.** Say "storage on this computer", not "local backend". An
   error says what happened and what to do next.
3. **Say where the data is**, and whose data is open.
4. **Claim only what is true.** If we can't tell whether a sync worked, we
   don't say it did. Not every app works offline: Chat needs a server.
5. **Losing data is the worst failure.** When two copies differ and we can't
   tell which is newer, we keep both or ask.
6. **No privacy theatre.** We don't add a password screen that a person with
   access to the files can walk around.
7. **Gaps found in machin go upstream.** We report them in the
   [machin repository](https://github.com/javimosch/machin/issues) instead of
   only working around them.

## Accounts

**A local account is not required, and there is none today.**

People who share one computer login share Machin 365 data. For privacy between
people, use separate computer logins.

**Optional profiles**, without passwords, could later keep work and personal
data apart. They would organise data and would not protect it. We build them
only when someone needs them. A real lock would need its own design for
encrypting data and protecting its keys.

## Not the goal

- Copying Microsoft 365 feature for feature.
- Requiring a hosted service to use your own data.
- A mandatory sign-up.
- One program that does everything. Apps stay separate and small.

## Open questions

- Which languages? The launcher is English only.
- Should Chat come with a server a non-technical person can use? Today they
  need one that somebody else runs.
- Where would sync point for a non-technical person?
