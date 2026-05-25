
import os
import sys
import http.server
import socketserver

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

def start_http_server():
    """Quietly runs the web server in the background"""
    web_dir = get_web_dir()
    os.chdir(web_dir)
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
            
    with socketserver.TCPServer(("127.0.0.1", 8000), QuietHandler) as httpd:
        httpd.serve_forever()