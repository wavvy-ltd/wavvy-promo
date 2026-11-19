#!/usr/bin/env python3
"""Record each voice line with Kokoro (am_michael) via hyperframes tts; write durations back.
Only re-records lines whose wav is missing or whose text changed."""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.environ["HYPERFRAMES_PYTHON"] = "/root/.venvs/audio/bin/python"
sb = json.load(open("storyboard.json"))
os.makedirs("assets/audio", exist_ok=True)
for vo in sb["voice"]:
    out = vo["src"]
    if vo.get("duration") and os.path.exists(out):
        continue
    r = subprocess.run(["npx", "--yes", "hyperframes@0.8.186", "tts", vo["text"], "-v", "am_michael", "-s", "1.0", "-o", out, "--json"],
                       capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith("{")]
    if not lines:
        print(r.stdout[-800:], r.stderr[-800:]); raise SystemExit(1)
    vo["duration"] = round(json.loads(lines[-1])["durationSeconds"], 2)
    print(f"{vo['id']:>4} {vo['start']:5.1f} +{vo['duration']:4.2f} -> {vo['start']+vo['duration']:5.1f}  {vo['text']}")
json.dump(sb, open("storyboard.json", "w"), indent=2, ensure_ascii=False)
