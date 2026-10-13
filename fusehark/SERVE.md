# FuseHark serve (host-supervised)
- Run `fusehark/SERVE.bat` (or Task Scheduler at logon, restart-always).
- Health: `http://localhost:4103/health` -> `{"status":"ok"}`.
- Phone path: `http://<laptop-lan-ip>:4103/hearing/chunk` + `X-Fuse-Token`.
- Firewall: admin-run once `New-NetFirewallRule -DisplayName FuseHark-ingest-4103 ...4103...`.
- Why host, not container: server shells `docker exec osd-postgres psql`
  and reads osd-services/.env — containerizing needs a TCP DB driver.
- Token rotation: change `.env` FUSEHARK_TOKEN, restart this script.
