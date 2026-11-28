#!/usr/bin/env bash
# check-portable.sh <binary> — the binary must survive a hostname lookup on a
# system older than the build's (javimosch/machin#764).
# A failed login is the expected outcome (exit 1); 136 is the crash.
#
# A bare container cannot show it: the crash needs a name-service plugin that
# a glibc binary loads from the host. Desktops ship one (mDNS), so each image
# gets libnss-mdns before the lookup.
set -euo pipefail
bin="$(readlink -f "${1:?usage: check-portable.sh <binary>}")"
for image in ubuntu:22.04 ubuntu:24.04; do
    code=0
    docker run --rm -v "$bin:/machin-365:ro" \
        -e MACHIN_365_HOME=/tmp/suite -e MACHIN_365_TELEMETRY=0 "$image" bash -c '
            { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libnss-mdns; } >/dev/null 2>&1 || exit 90
            grep -q "^hosts:.*mdns4_minimal" /etc/nsswitch.conf || exit 91
            echo x | /machin-365 auth login --server http://nosuchhost.invalid \
                --email probe@example.com --password-stdin >/dev/null 2>&1' || code=$?
    echo "$image: exit $code"
    [ "$code" -eq 1 ] || { echo "::error::hostname lookup on $image: expected exit 1, got $code (90/91: the check could not be set up)"; exit 1; }
done
