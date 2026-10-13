@echo off
REM FuseHark ingest — host-supervised server (port 4103, LAN-open for phone).
REM Schedule: Task Scheduler at logon (restart always) OR run manually.
REM Requires: Docker fleet up (osd-postgres), .env with FUSEHARK_TOKEN.
set FUSEHARK_PORT=4103
python3 "C:\Users\gotha\DevOpsBrain\fusehark\backend\fusehark_ingest.py"
