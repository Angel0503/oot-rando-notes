
import os
import sys
import http.server
import socketserver

def get_web_dir():
    """Finds the 'web' folder, even when bundled inside a .exe"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'web')

def start_http_server():
    """Quietly runs the web server in the background"""
    web_dir = get_web_dir()
    os.chdir(web_dir)
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
            
    with socketserver.TCPServer(("127.0.0.1", 8000), QuietHandler) as httpd:
        httpd.serve_forever()