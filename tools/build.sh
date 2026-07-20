#!/usr/bin/env bash
#
# Package the watch face into a distributable archive.
#
# Assembles the on-device layout (manifest + descriptors + assets + preview)
# into dist/, then zips it. The final artifact usually needs to be renamed to
# the Huawei watch-face extension (and, for sideloading, signed) — see README.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE="$ROOT/dist/watchface"
OUT="$ROOT/dist/my-watch.zip"

echo "==> Cleaning stage dir"
rm -rf "$STAGE" "$OUT"
mkdir -p "$STAGE"

echo "==> Copying descriptors"
# On-device the manifest is named `Com.Huawei.watchface` (no extension).
cp "$ROOT/src/manifest.xml"   "$STAGE/Com.Huawei.watchface"
cp "$ROOT/src/watchface.xml"  "$STAGE/watchface.xml"

echo "==> Copying assets"
cp -r "$ROOT/assets/." "$STAGE/"

echo "==> Copying preview"
if [ -f "$ROOT/preview/preview.png" ]; then
  cp "$ROOT/preview/preview.png" "$STAGE/preview.png"
else
  echo "    WARNING: preview/preview.png not found — the picker preview will be blank."
fi

echo "==> Zipping -> $OUT"
( cd "$STAGE" && zip -rq "$OUT" . )

echo "==> Done: $OUT"
echo "    Next: rename to the Huawei watch-face extension and sign if sideloading."
