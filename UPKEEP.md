# OSD recurring upkeep (weekly Monday + monthly + TTL-driven)
# Weekly (Monday, ~15 min): `python sentinel/sentinel.py osd-services` (fast engines+lenses+asserts);
#   review OPEN-HIGH, triage wont-fix/false-positive with justification.
#   `docker compose config -q` + endpoint sweep (8 URLs) after any change.
# Monthly (1st, ~1h): Trivy full-fleet HIGH/CRITICAL (one image per call, persist cache);
#   `docker pull <tag>` + digest re-pin review; restic B2 copy + `forget --prune` verify;
#   `docker system df` + prune if C: < 15GB.
# Nightly SBOM (22:00, ~10 min): `python sentinel/engines/sbom.py nightly`
#   (export+dir scan per running container, grype re-match; penpot-be via SBOM not Trivy-direct).
# Weekly restore drill (Sun 03:00, ~5 min): `python infra/restore_drill.py`
#   (dump size + gzip integrity + throwaway-PG restore + row-count; verified 2026-10-08).
# TTL-driven: briefs refresh at 30d (`breakthrough_finder.py check`); TaskSpec build-tier
#   blocks on STALE automatically. Renovate (once activated) replaces manual digest review.
# Quarterly: rotate .env secrets (URL-safe alphabet), verify restore from B2 snapshot.
