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
    with open("url_config.yaml", "r") as file_object:
        return yaml.safe_load(file_object)

class handle(BaseHTTPRequestHandler):
    def do_GET(self):
        # print (self.requestline, self.path)
        query = urllib.parse.unquote(self.path[1:]) # remove leading '/' in path
        query_components = query.split(" ", 1)
        if query_components[0] in dataMap:
            type = query_components[0]
            query_args = query_components[1] if len(query_components) > 1 else ""
        elif query_components[0] == '_ls':
            self.process_ls()
            return
        else:
            type = 'g'
            query_args = query

        query_args = urllib.parse.quote_plus(query_args)
        redirect_url = dataMap[type] + query_args
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", redirect_url)
        self.end_headers()
    
    def process_ls(self):
        self.send_response(HTTPStatus.FOUND)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("url_config.yaml", "r") as file_object:
            content = "<html><body><pre>{}</pre></body></html>".format(file_object.read())
        response = bytes(content, 'utf-8')
        self.wfile.write(response)

if __name__ == "__main__":
    dataMap = load_config()
    run('localhost', 12345, handle)
