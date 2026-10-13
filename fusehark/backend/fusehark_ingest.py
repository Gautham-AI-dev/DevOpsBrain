"""FuseHark ingest + recall (stdlib only). OSD-side endpoint for phone sync.
Runs on OSD laptop (host python3). Phone POSTs direct (LAN or WireGuard):
  POST /hearing/chunk {profile, kind, ts_start, ts_end?, title?, content,
                       tags?, speakers?} + X-Fuse-Token  -> {id}
  POST /hearing/brief {profile, date, markdown}           -> {id}
  GET  /hearing/recall?profile=&q=&since=&until=          -> [entries]
  GET  /health -> {ok}
Auth: per-profile token = HMAC(OPERATOR_MASTER, mission:account:tier:epoch)
  via operator/tokens.py (tier=read, account=fusehark-<profile>).
Storage: osd-postgres fusehark_chunks (+ vectors sidecar ready, embeddings
  arrive with phone payload or via nomic-embed-text backfill).
Timeline: date-bucketed; recall filters time/person(q)/topic(q substring).
"""
import hashlib
import hmac
import json
import os
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("FUSEHARK_PORT", "4103"))
PSQL = ["docker", "exec", "-i", "osd-postgres", "psql", "-U", "osd",
        "-d", "osd_main", "-tAc"]


def load_env():
    # .env lives in osd-services (single secrets file); backend moved to
    # fusehark/ project dir, so resolve absolutely, not relative to HERE.
    for cand in (os.path.join(os.path.dirname(HERE), ".env"),
                 r"C:\Users\gotha\DevOpsBrain\osd-services\.env"):
        try:
            vals = {}
            with open(cand, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        vals[k.strip()] = v.strip()
            return vals
        except OSError:
            continue
    return {}


ENV = load_env()
TOKEN = ENV.get("FUSEHARK_TOKEN", "")


def psql(sql):
    p = subprocess.run(PSQL + [sql], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=30)
    return p.stdout.strip()


def esc(s):
    return (s or "").replace("'", "''")


def do_chunk(body):
    for k in ("profile", "kind", "ts_start", "content"):
        if k not in body or not body[k]:
            return 400, {"error": f"missing {k}"}
    sql = ("INSERT INTO fusehark_chunks (profile, kind, ts_start, ts_end, title,"
           " content, tags, speakers) VALUES ('{}','{}','{}',{},{},'{}','{}','{}')"
           " RETURNING id;".format(
               esc(body["profile"]), esc(body["kind"]), esc(body["ts_start"]),
               f"'{esc(body['ts_end'])}'" if body.get("ts_end") else "NULL",
               f"'{esc(body['title'])}'" if body.get("title") else "NULL",
               esc(body["content"]), esc(",".join(body.get("tags", []))),
               esc(body.get("speakers", ""))))
    out = psql(sql)
    try:
        rid = int(out.split()[0])
    except (ValueError, IndexError):
        return 502, {"error": f"db insert failed: {out[:200]}"}
    return 200, {"ok": True, "id": rid}


def do_recall(qs):
    profile = qs.get("profile", [""])[0]
    q = qs.get("q", [""])[0]
    since = qs.get("since", ["1970-01-01"])[0]
    until = qs.get("until", ["2100-01-01"])[0]
    clauses = [f"ts_start >= '{esc(since)}'", f"ts_start <= '{esc(until)}'"]
    if profile:
        clauses.append(f"profile = '{esc(profile)}'")
    if q:
        clauses.append(f"(content ILIKE '%{esc(q)}%' OR title ILIKE '%{esc(q)}%' "
                       f"OR speakers ILIKE '%{esc(q)}%')")
    sql = ("SELECT id, profile, kind, ts_start, title, left(content, 300) FROM "
           f"fusehark_chunks WHERE {' AND '.join(clauses)} "
           "ORDER BY ts_start DESC LIMIT 50;")
    out = psql(sql)
    rows = [dict(zip(("id", "profile", "kind", "ts", "title", "snippet"),
                     [c.strip() for c in line.split("|")]))
            for line in out.splitlines() if "|" in line]
    return 200, {"ok": True, "count": len(rows), "entries": rows}


class Handler(BaseHTTPRequestHandler):
    server_version = "fusehark-ingest/1.0"

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            self._send(200, {"status": "ok", "service": "fusehark-ingest"})
        elif u.path == "/hearing/recall":
            code, obj = do_recall(parse_qs(u.query))
            self._send(code, obj)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if TOKEN and not hmac.compare_digest(
                self.headers.get("X-Fuse-Token", ""), TOKEN):
            self._send(401, {"error": "bad token"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            length = 0
        if length <= 0 or length > 500000:
            self._send(400, {"error": "bad body"})
            return
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._send(400, {"error": "invalid json"})
            return
        if self.path in ("/hearing/chunk", "/hearing/brief"):
            if self.path == "/hearing/brief":
                body = {"profile": body.get("profile", ""),
                        "kind": "brief",
                        "ts_start": body.get("date", "") + "T00:00:00+00",
                        "title": f"brief {body.get('date','')}",
                        "content": body.get("markdown", "")}
            code, obj = do_chunk(body)
            self._send(code, obj)
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"fusehark-ingest on :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
