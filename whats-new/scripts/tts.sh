#!/bin/bash
# Record every voice line in storyboard.json with Kokoro (via `hyperframes tts`) and write the
# measured durations back, so build.py can place the clips exactly.
#   scripts/tts.sh [voice]      default voice af_heart; needs `pip install kokoro-onnx soundfile`
set -euo pipefail
cd "$(dirname "$0")/.."
VOICE=${1:-af_heart}
mkdir -p assets/audio
python3 - "$VOICE" <<'EOF'
import json, subprocess, sys
voice = sys.argv[1]
sb = json.load(open("storyboard.json"))
for vo in sb.get("voice", []):
    out = vo.get("src") or f"assets/audio/{vo['id']}.wav"
    r = subprocess.run(["npx", "--yes", "hyperframes@0.8.186", "tts", vo["text"], "-v", voice, "-o", out, "--json"],
                       capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("{")][-1]
    meta = json.loads(line)
    vo["src"], vo["duration"] = out, round(meta["durationSeconds"], 2)
    print(f"{vo['id']:>6}  {vo['duration']:5.2f}s  {vo['text'][:70]}")
json.dump(sb, open("storyboard.json", "w"), indent=2, ensure_ascii=False)
open("storyboard.json", "a").write("\n")
print("durations written to storyboard.json — now: python3 scripts/build.py")
EOF
