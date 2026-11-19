#!/bin/bash
# usage: act.sh NAME "question" -> ask; if a permission sheet shows, shot NAME_perm, Allow Once, wait, shot NAME_done
cd /root/.hermes/cache/scratch/wavvy-shots
./ask.sh "$1" "$2" | head -4
U=$(cat /root/.hermes/cache/scratch/wavvy-vmservice.uri)
if marionette --uri $U get-interactive-elements 2>/dev/null | grep -q 'Permission Required'; then
  cp "${1}_a.png" "${1}_perm.png"
  marionette --uri $U get-interactive-elements 2>/dev/null | grep -E '^Type: Text, Text' | sed -E 's/^Type: [A-Za-z]+, Text: "([^"]*)".*/  PERM: \1/' | tail -3
  marionette --uri $U tap --text "Allow Once" >/dev/null 2>&1
  prev=""; same=0
  for i in $(seq 1 40); do
    sleep 4
    cur=$(marionette --uri $U get-interactive-elements 2>/dev/null | md5sum)
    [ "$cur" = "$prev" ] && same=$((same+1)) || same=0; prev=$cur
    [ $same -ge 2 ] && break
  done
  marionette --uri $U take-screenshots -o "${1}_done.png" >/dev/null 2>&1
  if marionette --uri $U get-interactive-elements 2>/dev/null | grep -q 'Permission Required'; then echo "  (another permission pending)"; fi
fi
