#!/bin/bash
# Render the promo and normalise it for social (−15 LUFS integrated, −1 dBTP true peak).
# Usage: scripts/deliver.sh [out-basename] [composition.html] [raw]
#   → <out>.mp4 (raw render) and <out>-social.mp4. The second arg renders an alternative root
#   (e.g. variants/sfx-only.html); "raw" as the third arg skips loudness normalisation, which
#   is wrong for a sparse effects-only track.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=${1:-wavvy-promo-60s}
COMP=${2:-index.html}
MODE=${3:-social}

npx --yes hyperframes@0.8.186 render -c "./$COMP" --quality delivery --output "$OUT.mp4"
if [ "$MODE" = "raw" ]; then
  npx --yes hyperframes@0.8.186 audio "$OUT.mp4" --json | python3 -c '
import json,sys; d=json.load(sys.stdin)["items"][0]; print("delivered (raw):", d["duration"], "s", d["loudness"])'
  exit 0
fi

# two-pass loudnorm with linear gain only (no dynamic processing), video stream copied
MEASURED=$(ffmpeg -v info -i "$OUT.mp4" -af loudnorm=I=-15:TP=-1:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
read -r I TP LRA THRESH OFFSET < <(printf '%s' "$MEASURED" | python3 -c '
import json,sys; m=json.load(sys.stdin)
print(m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])')
ffmpeg -v error -y -i "$OUT.mp4" -c:v copy \
  -af "loudnorm=I=-15:TP=-1:LRA=9:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$THRESH:offset=$OFFSET:linear=true" \
  -c:a aac -b:a 192k "$OUT-social.mp4"

npx --yes hyperframes@0.8.186 audio "$OUT-social.mp4" --json | python3 -c '
import json,sys; d=json.load(sys.stdin)["items"][0]; print("delivered:", d["duration"], "s", d["loudness"])'
