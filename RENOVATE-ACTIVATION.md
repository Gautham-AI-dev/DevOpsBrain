# Renovate activation (operator step, ~10 min)
# Config already at DevOpsBrain/renovate.json (weekly Monday, no-automerge, digest pins).
# Runner image pinned: renovate/renovate@sha256:f2209c61a9c3c8c74ac58eecb5f15ec43651f1ba694aa33493ff2062b90ff4d3 (39, 2026-10-08).
# Option A (GitHub App, recommended for private repos):
#   1. Install Renovate GitHub App on the repo/org.
#   2. Add RENOVATE_TOKEN secret if using self-hosted runner; else Mend-hosted needs no runner.
# Option A (GitHub App, recommended for private repos):
#   1. Install Renovate GitHub App on the repo/org.
#   2. Add RENOVATE_TOKEN secret if using self-hosted runner; else Mend-hosted needs no runner.
# Option B (self-hosted runner on this laptop, free, works for local-only repos):
#   1. `npm i -g renovate` (or docker run renovate/renovate).
#   2. Weekly Task Scheduler: `renovate --platform=local --autodiscover=false DevOpsBrain`
#      with RENOVATE_TOKEN=(GitHub PAT, only for release-note fetching; compose bumps need no token).
#   3. Review PRs/MRs Monday; merge digest bumps after `docker compose config -q` + smoke.
# Until activated: manual monthly `docker pull <img>:<tag>` + digest re-pin (see notes).
