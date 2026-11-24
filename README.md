# machin-365

The Machin app suite: one CLI that installs and runs the machin-* desktop apps,
with optional sync to a [machin-bkn](https://github.com/javimosch/machin-bkn)
server. 100% open source.

Every app is **offline-first** — it works fully on local data and syncs when a
server is configured. The suite itself is a single small native binary written
in [MFL](https://github.com/javimosch/machin).

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/javimosch/machin-365/HEAD/install.sh | sh
machin-365 init
machin-365 catalog                  # apps in the catalog + install state
machin-365 install tasks            # release asset, or:
machin-365 install tasks --bin ./build/machin-tasks   # local build
machin-365 run tasks                # launch (also in your OS app menu)
```

Or build from source (needs `machin` on PATH):

```sh
git clone https://github.com/javimosch/machin-365
cd machin-365 && ./build.sh         # static binary → build/machin-365
```

## Use

```sh
machin-365 catalog [--refresh]      # apps + install state; --refresh pulls ${server}/catalog.json
machin-365 install tasks            # release asset, or:
machin-365 install tasks --bin ./build/machin-tasks   # local build
                                  # (--bin must name the app's own binary —
                                  #  basename is checked against the catalog)
machin-365 uninstall tasks          # remove app; data/tasks/ is kept
machin-365 prune                     # drop .desktop entries whose home/binary is gone
machin-365 run tasks                # launch (also in your OS app menu)
machin-365 auth login --server URL --email E [--password P | --password-stdin] [--org SLUG]
machin-365 auth signup --server URL --email E [--password P | --password-stdin] [--name N] [--org SLUG]
machin-365 auth memberships | orgs       # orgs the account belongs to
machin-365 auth org create <slug> [--name N]   # create an org (creator becomes owner)
machin-365 auth member add <org> <user> [--role owner|admin|member]
machin-365 auth member list <org> | member remove <org> <user>
machin-365 auth switch-org <slug>       # re-scope the session, no password
machin-365 auth status | logout
machin-365 config                   # paths + account state
machin-365 config set sync_collections m365/tasks,sync/tombstones
                                  # sticky sync collection list
machin-365 service install              # fetch latest mbkn release, install + start local bkn
machin-365 service install --bin ./bkn  # or a local bkn/mbkn binary
machin-365 service install --latest     # upgrade bkn to the newest release
machin-365 service start|stop|status     # manage local bkn (127.0.0.1:17630)
machin-365 sync                     # replicate local bkn <-> remote bkn
machin-365 sync --watch 15          # continuous replication every 15s
machin-365 version                  # suite version stamp (also: --version, -V)
machin-365 update                   # self-update to the latest GitHub release
```

## Demo server

A shared demo instance is running at `https://machin-bkn.vps1.intrane.fr`
([machin-bkn](https://github.com/javimosch/machin-bkn)) with open signup —
each account gets its own org-scoped workspace, so users can't see each
other's data. Try the whole flow:

```sh
machin-365 auth signup --server https://machin-bkn.vps1.intrane.fr \
    --email you@example.com    # password: no-echo prompt (or --password-stdin)
machin-365 catalog --refresh   # when the server hosts /catalog.json
machin-365 install tasks
machin-365 service install   # downloads latest mbkn release, verifies + starts local bkn
machin-365 sync                # discovers collections via GET /v1/collections
machin-365 run tasks            # add a task, sync, see it on the server
```

`auth signup` registers the account, creates a personal org (you become
owner), and logs in with org-scoped tokens. The password never has to sit
in argv: omit `--password` on a terminal and you get a no-echo prompt;
scripts pipe it instead — `echo -n "$PW" | machin-365 auth login ...
--password-stdin` (same flag on `signup`, matching bkn's auth commands).
`--password P` still works for scripts, but on a terminal the CLI warns
that argv lands in shell history and `ps`. Tenancy is enforced server-side:
the bkn `org` access policy stamps and filters rows by the caller's org, so
sync needs no per-user configuration — each account only ever sees its own
collections' rows. A shared throwaway demo login also exists
(`demo@machin-365.dev` / org `demo`) for quick poking.

Sync is org-scoped, so sharing a workspace means sharing an org. An org
owner/admin adds a teammate with `auth member add <org> <email>`; the
teammate then signs in with `auth login --org <slug>` (or
`auth switch-org <slug>` when already logged in) and sync converges on the
same rows. `auth memberships`/`auth orgs` show which orgs an account can
enter, `auth member list` shows an org's roster. An account with no orgs —
e.g. one whose signup org-create step failed — creates its own workspace
with `auth org create <slug>` (the creator becomes owner; an org-less
session is scoped to it automatically).

## Local-first data layer

`service *` runs a suite-managed **local bkn** — the default backend every app
talks to, so apps work fully offline and cannot tell whether a remote server
exists. `sync` then replicates all store collections between the local and the
remote bkn configured via `auth login`.

Data created before the first sign-in is kept: the local store is
partitioned per account, and the pre-auth (`_unclaimed`) store is adopted
into the first account's store at `auth signup`/`auth login` — merged when
the account already has local data, renamed into place otherwise — so
offline-first records are never silently stranded.

`service install` resolves the bkn binary in order: `--bin /path/to/bkn`,
then `$MACHIN_BKN_BIN`, then `bkn`/`mbkn` on PATH, then an existing suite
install — and finally downloads the latest
[machin-bkn](https://github.com/javimosch/machin-bkn) release asset for your
platform, verified against the release's published checksum and probed like
any other install. Because an existing suite install wins that resolution,
a bare re-run never reaches the release channel — pass
`service install --latest` (alias `--upgrade`) to fetch and install the
newest release regardless of what is already installed. To use a locally
built binary instead, pass `--bin` —
build it from the machin-bkn repo (needs the `machin` toolchain).

Replication is one pass per invocation (`--watch N` loops every N seconds),
last-writer-wins on an app-level `_mtime` field (POST upserts by record id).
Only one `sync` runs per suite home at a time — a second invocation
(including a second `--watch`) fails fast with `sync already running
(pid N)`; the `.sync.lock` dir in the suite home is reclaimed
automatically when its holder dies.
`_mtime` is trusted only up to a skew horizon of **15 minutes** past now:
a stamp beyond that (client clock skew, a unit bug writing µs/ns) is
rewritten to the current time when sync writes the doc, and reads treat
it as the horizon — a poisoned future timestamp degrades to "recent"
instead of winning every conflict and every tombstone forever. Each pass
prints a one-line warning when it rewrites stamps, so the bad writer
surfaces. Tombstone markers get a wider horizon so a back-filled delete
marker is always stamped just past the record it deletes.

Which collections sync is sticky configuration: `--collections a/b,c/d` is
remembered in `config.json` (`sync_collections`) on first use, and
`config set sync_collections a/b,c/d` sets it explicitly — either way bare
`sync` / `sync --watch` keep working without retyping the list. Refs must be
`ns/coll` — a malformed entry is rejected with exit 2 and never persisted,
and the list is only saved after a pass completes without call failures.
With no configured set, sync probes `GET /v1/collections` on both sides;
`--collections` remains the override for servers without that route.

**Deletes propagate via tombstones**: before deleting a synced doc, the app
POSTs `{"ref":"ns/coll","id":"ns/coll|<id>","_mtime":T}` to the
`sync/tombstones` collection — the tombstone's own doc id is the compound
`ref|id`, so same-id deletes in different collections cannot overwrite each
other — then DELETEs the record. `sync/tombstones` is itself a synced
collection, so markers replicate like any doc; a record older than its
tombstone is deleted on both sides, while a newer `_mtime` (edit after
delete) wins and the record survives. Legacy tombstones written with a
bare target `.id` are still honoured and are rewritten to the compound id
on each sync pass. Apps that skip the tombstone will see deletes
resurrect — tombstone first, then delete. As a safety net, sync keeps
manifests of last-seen ids on both sides per account+endpoint identity
(`sync-manifest.<key>.txt` / `sync-remote-manifest.<key>.txt`, so an
account/org switch parks the old baseline instead of discarding it) and
writes the missing tombstone markers itself when a synced record
vanishes on either side — so deletes made through the store API by
scripts, agents, or other clients propagate too, with a one-line warning
per pass. Remote-side detection only fires on a complete, non-empty
remote fetch, so a wiped/rebuilt remote collection is restored from
local rather than deleting every device's data. The merge itself is
gated the same way: when either side's fetch fails or comes back
partial, pushes and pulls for that collection are skipped until a
complete fetch succeeds — a record missing from a partial view is
unseen, not absent, so reconciling on it would overwrite newer copies
on the other side. The one exception is the private-admin refusal on
an undeclared collection, which counts as confirmed-absent and keeps
first-sync self-provisioning working. `service reset` clears
every identity's manifest so a wiped store is restored from remote
rather than deleted everywhere.

## Layout

```
$MACHIN_365_HOME (default ~/.local/share/machin-365)
├── apps/<id>/bin/     installed app binaries
├── bin/bkn            local bkn binary
├── bkn/bkn.db         local bkn database (+ bkn.pid, bkn.log)
├── data/<id>/         each app's local store (SQLite etc.)
├── config.json        server URL + auth tokens + local bkn token
├── catalog.json       last-used catalog snapshot
└── installed.json     id → version/bin registry
```

Installed apps also get a `.desktop` entry, so they appear in the OS app
menu — no custom launcher needed. Entries launch through `machin-365 run`
(service autostart included) with `MACHIN_365_HOME` baked in, and are
namespaced per suite home so multiple homes can coexist. Entries from a
non-default home carry the home's basename (or a hash when the basename
is generic) in `Name=` and the full home path in `Comment=`, so same-named
apps from different homes stay distinguishable in the menu; the default
home keeps the bare app name. Entries whose
suite home was deleted or whose launcher binary moved away are dead —
`init` sweeps them automatically and `machin-365 prune` does it on demand;
live entries belonging to other suite homes are left untouched.

## Catalog

`catalog.json` is the contract: app id, kind (`desktop`|`web`), repo, version,
and per-platform release assets `{platform, url, sha256}`. The bundled copy is
compiled into the binary at build time; `MACHIN_365_CATALOG=/path.json`
overrides it — that is also the seam a server-hosted catalog will use.

## Roadmap

- **Now**: CLI install/run/auth, local bkn lifecycle (`service *`),
  LWW replication with delete tombstones + `sync --watch`, desktop apps
  (tasks on local bkn, chat over ws://)
- **Next**: sync daemon/autostart, chat message persistence, tenant
  provisioning + quotas on the demo server, server-hosted catalog
- **Later**: web/PWA app flavors, desktop launcher shell

## License

MIT
