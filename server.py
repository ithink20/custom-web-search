#!/usr/bin/python3

import http.server, urllib, yaml, argparse, logging, time, typing, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse

#singleton pattern
class ConfigLoader:
    CONFIG_PATH = "url_config.yaml"
    singleton_instance = None

    def __init__(self):
        self._data_map = None
        threading.Timer(5, self.refresh_config_data_map).start()

    @classmethod
    def getInstance(cls):
        if not ConfigLoader.singleton_instance:
            ConfigLoader.singleton_instance = ConfigLoader()
        return ConfigLoader.singleton_instance

    def _load_config(self):
        logging.info("loading config from path: {}".format(ConfigLoader.CONFIG_PATH))
        with open(ConfigLoader.CONFIG_PATH, "r") as file_object:
            return yaml.safe_load(file_object)

    def get_data_map(self, force_load=False):
        if not self._data_map or force_load:
            self._data_map = self._load_config()
        return self._data_map

    def refresh_config_data_map(self):
        updated_config_data_map = None
        try:
            updated_config_data_map = self._load_config()
        except Exception as e:
            # ignore loading error during refresh (potentially getting updated)
            logging.error("Failed to load config during refresh: {}".format(e))
        if updated_config_data_map:
            self._data_map = updated_config_data_map
        threading.Timer(5, self.refresh_config_data_map).start()

    def get_config_raw_content(self):
        with open(ConfigLoader.CONFIG_PATH, "r") as file_object:
            return file_object.read()


def run(host_name, port_number, handler_class):
    server_address = (host_name, port_number)
    httpd = HTTPServer(server_address, handler_class)
    logging.info('Server running on port : {port}\n'.format(port=port_number))
    httpd.serve_forever()

class handle(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.debug("Input Request: {}".format(self.path))
        query = urllib.parse.unquote(self.path[1:]) # remove leading '/' in path
        query_components = query.split(" ", 1)
        config_data_map = ConfigLoader.getInstance().get_data_map()
        if query_components[0] in config_data_map:
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
        redirect_url = config_data_map[type] + query_args
        logging.debug("Redirect URL: {}".format(redirect_url))
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", redirect_url)
        self.end_headers()

    def process_ls(self):
        self.send_response(HTTPStatus.FOUND)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        config_content = ConfigLoader.getInstance().get_config_raw_content()
        content = "<html><body><pre>{}</pre></body></html>".format(config_content)
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
    run('localhost', args.port, handle)
