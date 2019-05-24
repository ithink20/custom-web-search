#!/usr/bin/python3

import http.server, urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse


def run(host_name, port_number, handler_class):
    server_address = (host_name, port_number)
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()

class handle(BaseHTTPRequestHandler):
    def do_GET(self):
        print (self.requestline, self.path)
        query = urllib.parse.unquote(self.path).split(" ", 1)
        print (query)
        type = query[0]
        if (type == '/g'):
            query_string = urllib.parse.quote_plus(query[1])
            search_url = "https://www.google.com/search?q=" + query_string
            response = "<html><body><body>{}</html>".format(search_url).encode('utf-8')
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", search_url)
            self.end_headers()
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()

if __name__ == "__main__":
    run('localhost', 12345, handle)
