"""A tiny decision service for lab 06 (standard library only): GET /health and POST /decide."""

import json
import os
import signal
from http.server import BaseHTTPRequestHandler, HTTPServer

THRESHOLD = float(os.getenv("DSCR_THRESHOLD", "1.25"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self._send(200, {"status": "ok"}) if self.path == "/health" else self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/decide":
            return self._send(404, {"error": "not found"})
        app = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        dscr = round(app["ebitda"] / app["debt_service"], 2)
        self._send(200, {"dscr": dscr, "decision": "APPROVE" if dscr >= THRESHOLD else "REFER"})

    def log_message(self, fmt, *args):  # structured, no request bodies (they may contain personal data)
        print(json.dumps({"event": "request", "path": self.path, "status": args[1] if len(args) > 1 else ""}))


def _stop(signum, frame):
    # As PID 1 in a container, Python ignores SIGTERM unless a handler is installed, so Kubernetes would wait the whole
    # grace period (30 s) and then kill the pod — old pods keep serving during a rollout. Exit promptly instead.
    raise SystemExit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _stop)
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
