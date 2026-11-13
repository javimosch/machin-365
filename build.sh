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

"$MACHIN" encode src/*.src > build/machin-365.mfl
"$MACHIN" build build/machin-365.mfl -o build/machin-365 --static
echo "built build/machin-365"
