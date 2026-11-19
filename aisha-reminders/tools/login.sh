#!/bin/bash
# Log in with the repo's tracked dev-API test account (.patrol.env) without echoing it.
set -e
D=/root/.hermes/cache/scratch/wavvy-shots
ENVF=/root/code/wavvy-wallet-mvp/.patrol.env
get() { grep "^$1=" "$ENVF" | head -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//"; }
typ() { python3 -I -c 'import sys,shlex; s=sys.argv[1]; print(shlex.quote(s.replace("%","\\%").replace(" ","%s")))' "$1"; }
$D/m.sh tap --type TextField >/dev/null
sleep 1
adb shell input text "$(typ "$(get USERNAME)")"
$D/m.sh tap --x 150 --y 440 >/dev/null
sleep 1
adb shell input text "$(typ "$(get PASSWORD)")"
echo typed
