#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cronjobscript.sh'))
HOST = '127.0.0.1'
PORT = int(os.environ.get('LOCAL_RUNNER_PORT', '8001'))


class RunnerHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/health':
            return self._send(200, {'status': 'ok'})
        return self._send(404, {'error': 'not found'})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/run':
            return self._send(404, {'error': 'not found'})

        if not os.path.isfile(SCRIPT_PATH):
            return self._send(500, {'error': f'script not found: {SCRIPT_PATH}'})

        try:
            # Execute via bash to avoid exec permission issues
            completed = subprocess.run(
                ['bash', SCRIPT_PATH],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            return self._send(200, {
                'returncode': completed.returncode,
                'stdout': completed.stdout,
                'stderr': completed.stderr,
            })
        except Exception as exc:
            return self._send(500, {'error': str(exc)})


def main():
    server = HTTPServer((HOST, PORT), RunnerHandler)
    print(f'Local runner listening on http://{HOST}:{PORT} (POST /run)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    sys.exit(main())


