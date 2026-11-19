#!/bin/bash
# Split the full story render into 6 standalone parts: chapter card + walkthrough + shared end card.
set -euo pipefail
cd "$(dirname "$0")/../renders"
S=${1:-wavvy-whats-new-story-v5-social.mp4}
mkdir -p parts
cuts=(16.08 47.51 62.9 92.85 110.16 133.87 160.65)
END_A=160.65; END_B=167.9
names=(kcb-mpesa mtn-momo-iphone tag-screen transaction-charges bill-reminders money-in-out-rwf)
for i in 0 1 2 3 4 5; do
  a=${cuts[$i]}; b=${cuts[$((i+1))]}
  fo=$(python3 -c "print(round($b-$a-0.3,3))")
  ffmpeg -v error -y -i "$S" -filter_complex \
    "[0:v]trim=$a:$b,setpts=PTS-STARTPTS[v1];[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.15,afade=t=out:st=$fo:d=0.3[a1];[0:v]trim=$END_A:$END_B,setpts=PTS-STARTPTS[v2];[0:a]atrim=$END_A:$END_B,asetpts=PTS-STARTPTS,afade=t=in:d=0.3[a2];[v1][a1][v2][a2]concat=n=2:v=1:a=1[v][a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
    "parts/wavvy-whats-new-$((i+1))-${names[$i]}.mp4"
  echo "part $((i+1)) done"
done
for f in parts/*.mp4; do
  echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f") $(ffmpeg -i "$f" -af loudnorm=print_format=summary -f null - 2>&1 | grep 'Input Integrated')"
done
