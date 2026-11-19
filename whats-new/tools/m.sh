#!/bin/bash
# usage: m.sh els | m.sh shot NAME | m.sh <marionette args...>
source /etc/profile.d/flutter-android.sh >/dev/null 2>&1
U=$(cat /root/.hermes/cache/scratch/wavvy-vmservice.uri)
cd /root/.hermes/cache/scratch/wavvy-shots
if [ "$1" = els ]; then
  marionette --uri $U get-interactive-elements 2>/dev/null | grep '^Type:' | sed -E 's/^Type: ([A-Za-z]+)(, Text: "([^"]*)")?.*bounds: \{"x":([0-9.]+),"y":([0-9.]+).*/\1 | \3 | \4,\5/' | cut -c1-160
elif [ "$1" = shot ]; then
  marionette --uri $U take-screenshots -o "$2.png" 2>/dev/null | tail -1
else
  marionette --uri $U "$@" 2>&1 | grep -v -E 'root|superuser|^  /|📎|^$' | tail -3
fi
