# FuseHark — open ambient companion (dedicated project under OSD/DevOpsBrain)

Hears everything (with permission), processes on-phone, saves TEXT briefings
in a calendar-timeline DB. OSD has exclusive access for personality/preferences;
any AI reads via open JSON + MCP.

## Layout
- `backend/` — OSD ingest + recall endpoint (fusehark_ingest.py, :4103).
- `app/` — Android MVP (Kotlin): AudioRecord 16k → Silero VAD → whisper.cpp
  tiny/base → Qwen3-0.6B briefings → Room/SQLite timeline → sync.
- `bridge/` — direct phone<->OSD sync (LAN POST; WireGuard remote; no cloud).
- `docs/` — hearing_spec.py (ingest contract), plan, research briefs.

## Status
- Backend schema live (fusehark_chunks + vectors); ingest :4103 healthy.
- Next: timeline recall verify → Android MVP → WireGuard profiles → E2E.
