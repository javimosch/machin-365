# machin-365

The Machin app suite: one CLI that installs and runs the machin-* desktop apps,
with optional sync to a [machin-bkn](https://github.com/javimosch/machin-bkn)
server. 100% open source.

Every app is **offline-first** — it works fully on local data and syncs when a
server is configured. The suite itself is a single small native binary written
in [MFL](https://github.com/javimosch/machin).

## Install

```sh
git clone https://github.com/javimosch/machin-365
cd machin-365 && ./build.sh          # needs `machin` on PATH
./build/machin-365 init
```

## Use

```sh
machin-365 catalog                  # apps in the catalog + install state
machin-365 install tasks            # release asset, or:
machin-365 install tasks --bin ./build/machin-tasks   # local build
machin-365 run tasks                # launch (also in your OS app menu)
machin-365 auth login --server URL --email E --password P [--org SLUG]
machin-365 auth status | logout
machin-365 config                   # paths + account state
machin-365 service install --bin ./bkn   # install local bkn binary
machin-365 service start|stop|status     # manage local bkn (127.0.0.1:17630)
machin-365 sync                     # replicate local bkn <-> remote bkn
```

## Local-first data layer

`service *` runs a suite-managed **local bkn** — the default backend every app
talks to, so apps work fully offline and cannot tell whether a remote server
exists. `sync` then replicates all store collections between the local and the
remote bkn configured via `auth login`.

Replication is one pass per invocation, last-writer-wins on an app-level
`_mtime` field (POST upserts by record id). **Deletes are not propagated yet** —
don't delete synced docs until tombstones land.

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
menu — no custom launcher needed.

## Catalog

`catalog.json` is the contract: app id, kind (`desktop`|`web`), repo, version,
and per-platform release assets `{platform, url, sha256}`. The bundled copy is
compiled into the binary at build time; `MACHIN_365_CATALOG=/path.json`
overrides it — that is also the seam a server-hosted catalog will use.

## Roadmap

- **Now**: CLI install/run/auth, local bkn lifecycle (`service *`),
  one-pass LWW replication (`sync`), desktop apps only
- **Next**: tasks app on the local bkn HTTP API, delete tombstones,
  sync loop/daemon mode, tenant provisioning + quotas on the demo server,
  server-hosted catalog
- **Later**: web/PWA app flavors, desktop launcher shell, `machin-365 update`

## License

MIT
