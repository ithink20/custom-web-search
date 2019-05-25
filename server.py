#!/usr/bin/python3

import http.server, urllib, yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse

dataMap = None

def run(host_name, port_number, handler_class):
    server_address = (host_name, port_number)
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()

def load_config():
    print("here")
    with open("url_config.yaml", "r") as data:
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as err:
            print(err)

class handle(BaseHTTPRequestHandler):
    def do_GET(self):
        # print (self.requestline, self.path)
        query = urllib.parse.unquote(self.path).split(" ", 1)
        type = query[0]
        flag = False
        for item in dataMap:
            if (item == type[1:]):
                query_string = urllib.parse.quote_plus(query[1])
                search_url = dataMap[item] + query_string
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", search_url)
                self.end_headers()
                flag = True
                break
        if not flag:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()

if __name__ == "__main__":
    dataMap = load_config()
    run('localhost', 12345, handle)
