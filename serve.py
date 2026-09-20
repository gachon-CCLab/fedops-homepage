from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=4313)
args=parser.parse_args()
root=Path(__file__).resolve().parent/'dist'
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip('/') == '/version-1':
            self.send_error(404)
            return
        super().do_GET()
    def do_HEAD(self):
        if self.path.rstrip('/') == '/version-1':
            self.send_error(404)
            return
        super().do_HEAD()
    def send_error(self,code,message=None,explain=None):
        if code==404 and (root/'404.html').is_file():
            data=(root/'404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(data)))
            self.end_headers()
            if self.command!='HEAD':self.wfile.write(data)
        else:super().send_error(code,message,explain)
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        super().end_headers()
    def log_message(self,*args):
        pass
server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(root)))
print(f'FedOps local preview: http://127.0.0.1:{args.port}/',flush=True)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
