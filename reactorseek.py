#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse

REGISTRY_FILE = os.path.expanduser("~/myinternet/sites.json")


def load_registry():

    if os.path.exists(REGISTRY_FILE):

        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}


class ReactorHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)

        params = urllib.parse.parse_qs(parsed.query)

        query = params.get("q", [""])[0].lower()

        registry = load_registry()

        content = ""

        content += "TITLE: ReactorSeek\n"

        content += "TEXT: Поиск по react:// интернету\n"

        content += "\n"

        content += "INPUT: search\n"

        content += "BUTTON: Искать|SEARCH\n"

        content += "\n"

        if query:

            found = False

            for name, url in registry.items():

                if query in name.lower():

                    found = True

                    content += f"LINK: {name}|react://{name}\n"

            if not found:

                content += "TEXT: Ничего не найдено\n"

        else:

            content += "TEXT: Все сайты:\n"

            for name in registry.keys():

                content += f"LINK: {name}|react://{name}\n"

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/plain; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(content.encode("utf-8"))

    def log_message(self, format, *args):
        pass


def main():

    port = 8080

    server = HTTPServer(
        ("0.0.0.0", port),
        ReactorHandler
    )

    print(f"ReactorSeek: react://search")
    print(f"http://127.0.0.1:{port}")

    server.serve_forever()


if __name__ == "__main__":
    main()
