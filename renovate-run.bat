@echo off
REM Renovate self-hosted runner (weekly): digest bumps for osd-services compose.
REM Needs: RENOVATE_TOKEN (GitHub PAT, release-notes only) in .env
REM Schedule: Task Scheduler weekly Monday 05:30 -> this file.
setlocal
cd /d C:\Users\gotha\DevOpsBrain
docker run --rm -v "%CD%:workspace" -e RENOVATE_TOKEN=%RENOVATE_TOKEN% ^
  -e LOG_LEVEL=info renovate/renovate:39 ^
  --platform=local --autodiscover=false --base-dir=/tmp/renovate workspace/osd-services
echo Review PRs/MRs Monday; merge digest bumps after compose config -q + smoke.
