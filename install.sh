#!/bin/sh
# install.sh — one-line installer for machin-365.
#
#   curl -fsSL https://raw.githubusercontent.com/javimosch/machin-365/HEAD/install.sh | sh
#
# Downloads the latest GitHub release binary for this platform into
# ~/.local/bin/machin-365 (override with MACHIN_365_BIN_DIR).
set -eu

REPO="javimosch/machin-365"
VERSION="${MACHIN_365_VERSION:-latest}"

os=$(uname -s | tr '[:upper:]' '[:lower:]')
arch=$(uname -m)
case "$arch" in
  x86_64|amd64) arch="amd64" ;;
  arm64|aarch64) arch="arm64" ;;
esac
platform="$os-$arch"

case "$platform" in
  linux-amd64|linux-arm64) ;;
  darwin-amd64|darwin-arm64)
    echo "install.sh: no darwin release assets published yet ('$platform')" >&2
    exit 1
    ;;
  *) echo "install.sh: unsupported platform '$platform'" >&2; exit 1 ;;
esac

if [ "$VERSION" = "latest" ]; then
  url="https://github.com/$REPO/releases/latest/download/machin-365-$platform"
else
  url="https://github.com/$REPO/releases/download/$VERSION/machin-365-$platform"
fi

dir="${MACHIN_365_BIN_DIR:-$HOME/.local/bin}"
mkdir -p "$dir"
tmp="$dir/.machin-365.download"

curl -fsSL "$url" -o "$tmp"
chmod +x "$tmp"
mv -f "$tmp" "$dir/machin-365"
echo "installed machin-365 -> $dir/machin-365"
echo "next: machin-365 init && machin-365 catalog"
