#!/usr/bin/env bash
# Download subtitles for every Video in playlist.txt into NNN.<lang>.txt (one caption line per line).
# Tries human English (en-IN) first, then YouTube's Hindi speech recognition (hi-orig).
# One language per request and long pauses, because YouTube returns 429 when asked too fast.
cd "$(dirname "$0")"
Y="${CAMPUSX_ENV:-$(conda info --base)/envs/campusx}/bin/python -m yt_dlp"
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
done < playlist.txt
