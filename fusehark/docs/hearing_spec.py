"""osd-hearing ingest endpoint (stdlib only): receives HearingBot chunks direct.
Runs on OSD laptop. Phone POSTs (same LAN or via WireGuard, no cloud relay):
  POST /hearing/chunk {profile, ts, text, speakers?, embedding?} -> stored
  POST /hearing/brief {profile, date, markdown} -> timeline DB
Auth: per-profile HMAC token (operator/tokens.py, tier=read, account=hearing-<profile>).
Storage: osd-postgres table hearing_chunks + vectors sidecar for embeddings.
Timeline: date-bucketed markdown + FTS query endpoint /hearing/recall?q=&since=
"""
