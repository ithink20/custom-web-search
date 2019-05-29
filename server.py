#!/usr/bin/python3

import http.server, urllib, yaml, argparse, logging, time, typing
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse

dataMap = None
CONFIG_PATH = "url_config.yaml"

def run(host_name, port_number, handler_class):
    server_address = (host_name, port_number)
    httpd = HTTPServer(server_address, handler_class)
    logging.info('Server running on port : {port}\n'.format(port=port_number))
    httpd.serve_forever()

def load_config():
    logging.info("loading config from path: {}".format(CONFIG_PATH))
    with open(CONFIG_PATH, "r") as file_object:
        return yaml.safe_load(file_object)

class handle(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.debug("Input Request: {}".format(self.path))
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
        logging.debug("Processing command: type({}), query_args({})".format(type, query_args))
        query_args = urllib.parse.quote_plus(query_args)
        redirect_url = dataMap[type] + query_args
        logging.debug("Redirect URL: {}".format(redirect_url))
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", redirect_url)
        self.end_headers()
    
    def process_ls(self):
        self.send_response(HTTPStatus.FOUND)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(CONFIG_PATH, "r") as file_object:
            content = "<html><body><pre>{}</pre></body></html>".format(file_object.read())
        response = bytes(content, 'utf-8')
        self.wfile.write(response)

if __name__ == "__main__":
    #parsing command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", help="port number to run server on", default=54321, type=int)
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    dataMap = load_config()
    run('localhost', args.port, handle)
