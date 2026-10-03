#!/usr/bin/env bash
# Copy of ../../transcripts/fetch.sh for the Deep Learning playlist: reads ../playlist.txt.
# Human English (en-IN) first, then YouTube's Hindi speech recognition (hi-orig). Resumable: skips Videos already fetched.
cd "$(dirname "$0")"
Y="/home/anshu/miniforge3/bin/python3 -m yt_dlp"
while IFS='|' read -r n id title; do
  ls "$n".*.txt >/dev/null 2>&1 && continue
  for try in "--write-subs en-IN" "--write-auto-subs hi-orig"; do
    set -- $try
    $Y -q --skip-download "$1" --sub-langs "$2" --sub-format vtt -o "$n" \
       "https://www.youtube.com/watch?v=$id" 2>>fetch.err
    sleep 45
    f=$(ls "$n".*.vtt 2>/dev/null | head -1)
    [ -n "$f" ] && break
  done
  [ -z "$f" ] && { echo "$n NO SUBS" >> fetch.err; continue; }
  grep -v -E '^$|-->|^WEBVTT|^Kind|^Language|^[0-9]+$' "$f" | sed 's/<[^>]*>//g' | awk '!seen[$0]++' > "${f%.vtt}.txt"
  rm -f "$n".*.vtt
done < ../playlist.txt
echo "DONE $(date)" >> fetch.log
