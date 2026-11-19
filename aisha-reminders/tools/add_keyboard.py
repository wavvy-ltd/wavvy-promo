"""Flutter (Marionette) screenshots leave the system keyboard area blank. Paste the real keyboard,
captured with `adb exec-out screencap` while the chat input was focused, into that area.
    python3 tools/add_keyboard.py assets/screens/rem/kb_screencap.png assets/screens/rem/*_q.png
"""
import sys
import numpy as np
from PIL import Image

kb = Image.open(sys.argv[1]).convert("RGB").resize((900, 2000))
ka = np.asarray(kb).astype(int)
# keyboard top in the screencap: first row (from 1100 down) whose mean differs from the app bg and stays dark-grey
def top_of_blank(a):
    m = a.mean(1)
    for y in range(1100, 1700):
        if np.abs(a[y:y + 40].mean((0, 1)) - [18, 18, 20]).max() < 3 and a[y:y + 40].std() < 4:
            return y
    return None

for f in sys.argv[2:]:
    q = Image.open(f).convert("RGB")
    y = top_of_blank(np.asarray(q).astype(int))
    if y is None:
        print(f, "no blank keyboard area, skipped")
        continue
    q.paste(kb.crop((0, y, 900, 2000)), (0, y))
    q.save(f)
    print(f, "keyboard pasted from y", y)
