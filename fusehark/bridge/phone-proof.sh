#!/data/data/com.termux/files/usr/bin/sh
# FuseHark phone proof — self-contained (no variables to lose).
curl -s -m 20 http://100.65.184.29:4103/hearing/chunk \
  -H "Content-Type: application/json" \
  -H "X-Fuse-Token: PASTE-FUSEHARK-TOKEN" \
  -d '{"profile":"pixel-phone","kind":"segment","ts_start":"2026-10-09T00:00:00+00:00","title":"phone proof","content":"Hello from phone hotspot test.","tags":["proof"],"speakers":"me"}'
echo
