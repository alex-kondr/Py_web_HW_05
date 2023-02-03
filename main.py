import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
from threading import Thread
from pathlib import Path
import logging 
import urllib

import server_websockets


SERVER_ADDRESS = ("0.0.0.0", 3000)
FILES_PATH = Path("exchange/template")
LIST_FILES = []


class HtttpHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parse_url = urllib.parse.urlparse(self.path)
        
        if parse_url.path == "/":
            self.send_file(FILES_PATH.joinpath("index.html"))
            
        elif parse_url.path[1:] in LIST_FILES:
            self.send_response(200)
            mt = mimetypes.guess_type(self.path)
                        
            self.send_file(FILES_PATH.joinpath(parse_url.path[1:]), mt=mt)
            
    def send_file(self, filename, status=200, mt: mimetypes="text/html"):
        self.send_response(status)
        self.send_header("Content-type", mt[0])
        self.end_headers()
        
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())            

                        
def run_http_server(server=HTTPServer, handler=HtttpHandler):
    http = server(SERVER_ADDRESS, handler)
    
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def find_files(html_path):
    
    for file in html_path.iterdir():
        if file.is_file():
            LIST_FILES.append(file.name)
            
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    
    find_files(FILES_PATH)    
       
    http_server = Thread(target=run_http_server)#, daemon=True)
    http_server.start()
    
    try:
        asyncio.run(server_websockets.main())
    except KeyboardInterrupt:
        http_server.terminate()