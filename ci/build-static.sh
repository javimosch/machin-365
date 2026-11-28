#!/usr/bin/env bash
# build-static.sh — the release build: a musl static binary, made in Alpine.
#
# A glibc --static binary is not portable: looking up a hostname makes it load
# the host's NSS modules and libc, and one built on Ubuntu 24.04 dies with
# SIGFPE on 22.04 (javimosch/machin#764). A musl binary loads nothing.
#
#   ci/build-static.sh /path/to/machin    -> build/machin-365
#
# Needs docker. The machin compiler comes from the host and runs in Alpine.
set -euo pipefail
cd "$(dirname "$0")/.."
machin="$(readlink -f "${1:?usage: build-static.sh /path/to/machin}")"
docker run --rm -v "$PWD:/src" -w /src -v "$machin:/usr/local/bin/machin:ro" \
    -e OWNER="$(id -u):$(id -g)" -e MACHIN_365_VERSION="${MACHIN_365_VERSION:-}" \
    alpine:3.22 sh -euc '
        apk add -q bash python3 git gcc musl-dev binutils openssl-dev openssl-libs-static \
            sqlite-dev sqlite-static zlib-dev zlib-static zstd-dev zstd-static
        git config --global --add safe.directory /src
        trap "chown -R $OWNER build src" EXIT
        ./build.sh
        strip build/machin-365
    '
