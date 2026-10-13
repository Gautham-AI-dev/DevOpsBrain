#!/data/data/com.termux/files/usr/bin/sh
# FuseHark hotspot proof v2 — self-diagnosing (prints every step).
# Usage: sh hotspot-proof.sh   (no variables needed, all values inline)
BASE="http://10.183.175.112:4103"
echo "[1] vars: BASE=$BASE"
echo "[2] health:"
curl -s -m 10 -o /dev/null -w "http=%{http_code} connect=%{time_connect}s\n" "$BASE/health"
echo "[3] chunk POST:"
curl -s -m 20 "$BASE/hearing/chunk" -H "Content-Type: application/json" -H "X-Fuse-Token: PASTE-FUSEHARK-TOKEN" -d '{"profile":"pixel-phone","kind":"segment","ts_start":"2026-10-09T00:00:00+00:00","title":"hotspot proof","content":"Hello via hotspot path.","tags":["proof"],"speakers":"me"}'
echo
echo "[4] done"
