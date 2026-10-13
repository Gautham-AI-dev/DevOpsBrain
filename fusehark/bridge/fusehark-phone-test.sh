#!/data/data/com.termux/files/usr/bin/sh
# FuseHark phone-side proof: POST one chunk + recall from Android (Termux).
# 1. Connect phone hotspot (already). 2. Replace TOKEN below.
# 3. sh fusehark-phone-test.sh
BASE="http://10.183.175.112:4103"
TOKEN="PASTE-FUSEHARK-TOKEN"
curl -s -m 20 "$BASE/hearing/chunk" -H "Content-Type: application/json" \
  -H "X-Fuse-Token: $TOKEN" \
  -d '{"profile":"pixel-phone","kind":"segment","ts_start":"2026-10-09T00:00:00+00:00","title":"phone proof","content":"Hello from phone hotspot test.","tags":["proof"],"speakers":"me"}'
echo
curl -s -m 20 "$BASE/hearing/recall?profile=pixel-phone&q=hotspot"
echo
