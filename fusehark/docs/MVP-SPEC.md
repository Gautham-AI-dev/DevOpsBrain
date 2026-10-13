# FuseHark Android MVP — spec v1 (2026-10-13)

## App (Kotlin, minSdk 29 / targetSdk 35)
- **Capture:** AudioRecord 16kHz/16-bit/mono, VOICE_RECOGNITION; mic-foreground-service
  (`foregroundServiceType="microphone"`), persistent notification, consent banner.
- **VAD gate:** Silero v6 ONNX (~2MB) via ONNX Runtime Mobile; 32ms frames;
  onset 0.6 / offset 0.35; 10-30s speech segments; silence discarded on-device.
- **On-device STT:** whisper.cpp tiny/base Q4 (draft transcripts, offline-first).
- **Briefings:** Qwen3-0.6B / SmolLM2-360M (decisions/actions/quotes/reminders + confidence).
- **Timeline DB:** Room/SQLite append-only `{id, ts_start/end, kind, title, content,
  tags, speakers}` + FTS; calendar-timeline UI; one-click export/delete.
- **Mic routing:** phone mic default; lav/BT/USB-C auto via OS audio routing.
- **Sync:** outbox table (SQLite, idempotency UUIDs, exp backoff) → POST chunks
  to OSD ingest (tailnet primary `http://100.65.184.29:4103`, LAN fallback);
  HMAC token from QR-provisioned secret; waveforms never leave phone by default.

## Consent & privacy (non-negotiable)
- Consent-mode ON default, per-person opt-out list, visible recording indicator,
  just-in-time permission rationale, versioned consent log, retention setting
  (default: transcripts 90d, audio never leaves device).

## Milestones
1. Capture+VAD+chunk pipeline (local only, no sync).
2. On-device STT + briefings + timeline UI.
3. Sync client (outbox + tailnet/LAN auto-select + token auth).
4. E2E: phone hears → TEXT → OSD timeline → recall → personality use.

## OSD side (done)
- Ingest :4103 (chunk/brief/recall, HMAC), schema live, both paths proven (id 6, 7).
