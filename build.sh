#!/usr/bin/env bash
# build.sh — compile the machin-365 CLI to a single native binary.
#
#   ./build.sh            → build/machin-365
#   MACHIN=/path/machin ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
MACHIN="${MACHIN:-machin}"
mkdir -p build

# Bundled catalog: generated from catalog.json, not committed
# (same pattern as machin-bkn's gen_qjs / the isomorphic boilerplate's host_gen).
python3 - <<'PY' > src/catalog_gen.src
import json
# ensure_ascii=False: MFL string literals are UTF-8 but do not decode \uXXXX
# escapes, so the default ascii escaping would land as literal "u2014" text.
print("func catalog_json() (s) {")
print("    s = " + json.dumps(open("catalog.json").read(), ensure_ascii=False))
print("}")
PY

# Suite version stamp: generated, not committed — same pattern as
# catalog_gen.src above. Resolution order: MACHIN_365_VERSION override,
# `git describe --tags --always` (the exact tag on release builds,
# nearest-tag + commit count + sha otherwise), a committed VERSION file
# for tarball builds, then "unknown" when no source exists at all.
VERSION="${MACHIN_365_VERSION:-}"
if [ -z "$VERSION" ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    VERSION="$(git describe --tags --always --dirty 2>/dev/null || true)"
fi
if [ -z "$VERSION" ] && [ -f VERSION ]; then
    VERSION="$(head -n 1 VERSION | tr -d '[:space:]')"
fi
[ -n "$VERSION" ] || VERSION="unknown"
python3 - "$VERSION" <<'PY' > src/version_gen.src
import json, sys
print("func cli_version() (s) {")
print("    s = " + json.dumps(sys.argv[1], ensure_ascii=False))
print("}")
PY

"$MACHIN" encode src/*.src > build/machin-365.mfl
"$MACHIN" build build/machin-365.mfl -o build/machin-365 --static
echo "built build/machin-365"
