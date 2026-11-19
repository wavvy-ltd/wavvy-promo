#!/bin/bash
# usage: ask.sh NAME "question" -> types via adb word by word, shots NAME_q, sends, waits for reply, shots NAME_a; prints reply texts
source /etc/profile.d/flutter-android.sh >/dev/null 2>&1
cd /root/.hermes/cache/scratch/wavvy-shots
U=$(cat /root/.hermes/cache/scratch/wavvy-vmservice.uri)
D="adb -s emulator-5554"
$D shell input tap 500 2242 >/dev/null 2>&1
sleep 1.2
first=1
for w in $2; do
  [ $first = 1 ] || $D shell input keyevent 62
  first=0
  e=$(printf '%s' "$w" | sed -e "s/'/\\\\'/g" -e 's/[&()?;<>|*$]/\\&/g')
  $D shell input text "$e"
done
sleep 1.5
marionette --uri $U take-screenshots -o "${1}_q.png" >/dev/null 2>&1
$D shell input tap 1020 2242
sleep 2.5
marionette --uri $U take-screenshots -o "${1}_t.png" >/dev/null 2>&1
prev=""; same=0
for i in $(seq 1 45); do
  sleep 4
  cur=$(marionette --uri $U get-interactive-elements 2>/dev/null | md5sum)
  [ "$cur" = "$prev" ] && same=$((same+1)) || same=0
  prev=$cur
  [ $same -ge 2 ] && break
done
marionette --uri $U take-screenshots -o "${1}_a.png" >/dev/null 2>&1
marionette --uri $U get-interactive-elements 2>/dev/null | grep -E '^Type: (Text|EditableText), Text' | sed -E 's/^Type: [A-Za-z]+, Text: "([^"]*)".*/\1/' | tail -14 | cut -c1-260
