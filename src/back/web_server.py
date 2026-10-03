import functools
import http.server
import os
import socketserver
import sys

DEFAULT_PORT = 8000
MAX_TRIES = 20  # tries 8000, 8001, ... if the port is already taken


def get_web_dir():
    """Finds the 'web' folder, even when bundled inside a .exe or placed in a subfolder"""
    if getattr(sys, 'frozen', False):
        # When running as a packaged .exe
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'web')
    else:
        # When running normally from Python
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        return os.path.join(parent_dir, 'web')


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def create_http_server():
    """Binds the web server on the first free port starting at 8000.
    Returns (server, port). Call server.serve_forever() (e.g. in a thread) to run it."""
    handler = functools.partial(QuietHandler, directory=get_web_dir())

    last_error = None
    for port in range(DEFAULT_PORT, DEFAULT_PORT + MAX_TRIES):
        try:
            return socketserver.TCPServer(("127.0.0.1", port), handler), port
        except OSError as e:  # port already in use
            last_error = e
    raise last_error


def start_http_server():
    """Quietly runs the web server in the background (kept for compatibility)"""
    httpd, _ = create_http_server()
    with httpd:
        httpd.serve_forever()