# machin-365

The Machin app suite: one CLI that installs and runs the machin-* desktop apps,
with optional sync to a [machin-bkn](https://github.com/javimosch/machin-bkn)
server. 100% open source.

Every app is **offline-first** — it works fully on local data and syncs when a
server is configured. The suite itself is a single small native binary written
in [MFL](https://github.com/javimosch/machin).

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/javimosch/machin-365/main/install.sh | sh
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
machin-365 uninstall tasks          # remove app; data/tasks/ is kept
machin-365 prune                     # drop .desktop entries whose home/binary is gone
machin-365 run tasks                # launch (also in your OS app menu)
machin-365 auth login --server URL --email E --password P [--org SLUG]
machin-365 auth signup --server URL --email E --password P [--name N] [--org SLUG]
machin-365 auth memberships | orgs       # orgs the account belongs to
machin-365 auth member add <org> <user> [--role owner|admin|member]
machin-365 auth member list <org> | member remove <org> <user>
machin-365 auth switch-org <slug>       # re-scope the session, no password
machin-365 auth status | logout
machin-365 config                   # paths + account state
machin-365 config set sync_collections m365/tasks,sync/tombstones
                                  # sticky sync collection list
machin-365 service install --bin ./bkn   # install local bkn (probes it runs + serves)
machin-365 service start|stop|status     # manage local bkn (127.0.0.1:17630)
machin-365 sync                     # replicate local bkn <-> remote bkn
machin-365 sync --watch 15          # continuous replication every 15s
```

## Demo server

A shared demo instance is running at `https://machin-bkn.vps1.intrane.fr`
([machin-bkn](https://github.com/javimosch/machin-bkn)) with open signup —
each account gets its own org-scoped workspace, so users can't see each
other's data. Try the whole flow:

```sh
machin-365 auth signup --server https://machin-bkn.vps1.intrane.fr \
    --email you@example.com --password a-good-password
machin-365 catalog --refresh   # when the server hosts /catalog.json
machin-365 install tasks
machin-365 service install --bin ./bkn   # install verifies + starts the local bkn
machin-365 sync --collections m365/tasks   # machin-bkn has no /v1/collections route
machin-365 run tasks            # add a task, sync, see it on the server
```

`auth signup` registers the account, creates a personal org (you become
owner), and logs in with org-scoped tokens. Tenancy is enforced server-side:
the bkn `org` access policy stamps and filters rows by the caller's org, so
sync needs no per-user configuration — each account only ever sees its own
collections' rows. A shared throwaway demo login also exists
(`demo@machin-365.dev` / org `demo`) for quick poking.

Sync is org-scoped, so sharing a workspace means sharing an org. An org
owner/admin adds a teammate with `auth member add <org> <email>`; the
teammate then signs in with `auth login --org <slug>` (or
`auth switch-org <slug>` when already logged in) and sync converges on the
same rows. `auth memberships`/`auth orgs` show which orgs an account can
enter, `auth member list` shows an org's roster.

## Local-first data layer

`service *` runs a suite-managed **local bkn** — the default backend every app
talks to, so apps work fully offline and cannot tell whether a remote server
exists. `sync` then replicates all store collections between the local and the
remote bkn configured via `auth login`.

Replication is one pass per invocation (`--watch N` loops every N seconds),
last-writer-wins on an app-level `_mtime` field (POST upserts by record id).

Which collections sync is sticky configuration: `--collections a/b,c/d` is
remembered in `config.json` (`sync_collections`) on first use, and
`config set sync_collections a/b,c/d` sets it explicitly — either way bare
`sync` / `sync --watch` keep working without retyping the list. With no
configured set, sync probes `GET /v1/collections` on both sides.

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
resurrect — tombstone first, then delete.

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
namespaced per suite home so multiple homes can coexist. Entries whose
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
- **Later**: web/PWA app flavors, desktop launcher shell, `machin-365 update`

## License

MIT
