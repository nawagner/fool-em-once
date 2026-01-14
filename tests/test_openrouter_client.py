import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer


class _Handler(BaseHTTPRequestHandler):
    last_headers = None
    last_body = None

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        _Handler.last_headers = dict(self.headers)
        _Handler.last_body = self.rfile.read(length).decode("utf-8")

        payload = {
            "choices": [
                {"message": {"content": "hello from openrouter"}}
            ]
        }
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


class OpenRouterClientTest(unittest.TestCase):
    def _start_server(self):
        server = HTTPServer(("127.0.0.1", 0), _Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        return server, thread

    def test_request_chat_completion_sends_key_and_returns_content(self):
        server, thread = self._start_server()
        try:
            base_url = f"http://127.0.0.1:{server.server_port}/api/v1"
            import sys
            from pathlib import Path

            repo_root = Path(__file__).resolve().parents[1]
            sys.path.insert(0, str(repo_root / "src"))

            import generate_essays  # noqa: E402

            content = generate_essays.request_chat_completion(
                model_id="test/model",
                messages=[{"role": "user", "content": "hi"}],
                api_key="test-key",
                base_url=base_url,
            )

            self.assertEqual(content, "hello from openrouter")
            self.assertIn("Authorization", _Handler.last_headers)
            self.assertEqual(_Handler.last_headers["Authorization"], "Bearer test-key")
            body = json.loads(_Handler.last_body)
            self.assertEqual(body["model"], "test/model")
            self.assertEqual(body["messages"], [{"role": "user", "content": "hi"}])
        finally:
            server.shutdown()
            server.server_close()

    def test_request_chat_completion_retries_on_500(self):
        class _FlakyHandler(BaseHTTPRequestHandler):
            call_count = 0

            def do_POST(self):
                _FlakyHandler.call_count += 1
                if _FlakyHandler.call_count == 1:
                    self.send_response(500)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"error":"temporary"}')
                    return

                payload = {
                    "choices": [
                        {"message": {"content": "recovered"}}
                    ]
                }
                body = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                return

        server = HTTPServer(("127.0.0.1", 0), _FlakyHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            base_url = f"http://127.0.0.1:{server.server_port}/api/v1"
            import sys
            from pathlib import Path

            repo_root = Path(__file__).resolve().parents[1]
            sys.path.insert(0, str(repo_root / "src"))

            import generate_essays  # noqa: E402

            content = generate_essays.request_chat_completion(
                model_id="test/model",
                messages=[{"role": "user", "content": "hi"}],
                api_key="test-key",
                base_url=base_url,
                max_retries=2,
                retry_sleep=lambda _: None,
            )

            self.assertEqual(content, "recovered")
            self.assertEqual(_FlakyHandler.call_count, 2)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
