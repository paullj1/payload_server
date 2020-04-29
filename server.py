#!/usr/bin/env python3

import argparse
import os
import random
import socket
import ssl
import string
import sys
import tempfile

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from signal import signal, SIGINT
from threading import Thread

class FPHandler(SimpleHTTPRequestHandler):
    server_version = 'Apache/2.2.14'
    sys_version = 'CentOS'

    def do_POST(req):
        length = req.headers['Content-Length']
        payload = req.rfile.read(int(length))
        req.rfile.close()
        with open("./logs/{}.txt".format(req.client_address[0]), "a") as fp_file:
            fp_file.write(payload.decode('utf-8'))
        req.send_response(200, "OK")
        req.end_headers()
        return True

    def do_GET(req):
        req.send_response(200, "OK")
        if 'app.js' in req.path:
            send_file(req, 'fp/app.js')
        elif is_valid_payload(req.path[1:]):
            send_file(req, os.path.join('payloads', req.path[1:]))
        elif req.path != '/favicon.ico':
            send_file(req, 'fp/index.html')
        return True

def is_valid_payload(filename) -> bool:
    if filename not in get_payloads():
        return False
    if not os.path.isfile(os.path.join('payloads',filename)):
        return False
    if filename[0] == '.':
        return False
    return True

def get_payloads():
    return os.listdir("payloads")

def send_file(req, filename):
    with open(filename, 'rb') as resource:
        resource_contents = resource.read()
        req.send_header('Content-Length', len(resource_contents))
        req.end_headers()
        req.wfile.write(resource_contents)

class FPServer():
    def __init__(self, args):
        signal(SIGINT, self.handler)
        self.args = args
        self.key_file = None
        self.cert_file = None
        self.httpd = None
        self.server_thread = None

    def handler(self, signal_received, frame):
        self.cleanup()

    def gen_certs(self):
        self.key_file = tempfile.NamedTemporaryFile()
        self.cert_file = tempfile.NamedTemporaryFile()
        key = self.key_file.name
        cert = self.cert_file.name
        os.system("openssl req -newkey rsa:2048 -nodes -keyout {} -x509 -days 90 -out {} -batch".format(key, cert))
        self.httpd.socket = ssl.wrap_socket(self.httpd.socket, keyfile=key, certfile=cert, server_side=True)

    def gen_links(self):

        if args.host:
            ips = args.host
        else:
            ips = os.popen("hostname --all-ip-addresses").read().split(' ')[0:-1]
            ips.append(socket.gethostname())

        rpath = ''.join(random.choice(string.ascii_letters) for i in range(10))
        proto = "http" if not args.ssl else "https"
        print("[+] Fingerprint link(s): (really, anything except a file that exists)")
        for ip in ips:
            print("{}://{}/".format(proto, ip))
            print("{}://{}/{}".format(proto, ip, rpath))

        print("\n[+] Available payloads:")
        for ip in ips:
            for f in get_payloads():
                if is_valid_payload(f):
                    print("{}://{}/{}".format(proto,ip,f))
        print()

    def cleanup(self):
        if self.httpd: # Must be threaded
            td = Thread(target=self.httpd.shutdown)
            td.start()
            self.server_thread.join()
            print("\n[-] Server shutdown... exiting")
        if self.key_file and self.cert_file:
            self.key_file.close()
            self.cert_file.close()

    def start(self):

        try:
            self.httpd = ThreadingHTTPServer(("", args.port), FPHandler)

            if self.args.ssl:
                self.gen_certs()

            self.gen_links()

            print("[+] Now all files in the 'payloads' directory and fingerprint server on port {}".format(args.port))
            self.server_thread = Thread(target=self.httpd.serve_forever)
            self.server_thread.start()
            
        except OSError as e:
            print("[!] Couldn't bind to port {}.  Probably in use.".format(args.port))
            self.cleanup()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Serves all files in './payloads'
    direcotry with optional self-signed cert, as well as a fingerprint server
    that mimics the apache 'It works!' page, but actually fingerprints a
    browser.""")
    parser.add_argument("-p" , "--port", type=int, default=8000)
    parser.add_argument("-s", "--ssl", action="store_true", help="Run server over SSL?")
    parser.add_argument("-n", "--host", type=str, nargs='+', help="Hostname[s] (or IP[s]) for generated links")
    args = parser.parse_args()

    fpserver = FPServer(args)
    fpserver.start()
    fpserver.server_thread.join()
