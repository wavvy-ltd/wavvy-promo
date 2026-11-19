#!/bin/bash
# Capture the current emulator/device screen into assets/screens/<name>.png (full resolution).
#   scripts/capture.sh home            → assets/screens/home.png
# The phone mockup crops `brand.phone.crop_top` px (default 66 at 732 px wide ≈ the status bar)
# and hides the bottom nav behind the bezel, so capture the whole screen as-is.
# Tip: `adb shell cmd statusbar collapse` first; `adb shell cmd statusbar expand-notifications`
# to capture a real notification; `adb emu sms send <sender> "<text>"` to inject an SMS.
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=${1:?name}
mkdir -p assets/screens
adb exec-out screencap -p > "assets/screens/$NAME.png"
python3 - "assets/screens/$NAME.png" <<'EOF'
import struct, sys
with open(sys.argv[1], "rb") as f:
    f.read(16); w, h = struct.unpack(">II", f.read(8))
print(f"{sys.argv[1]}: {w}x{h}")
EOF
