#!/usr/bin/env python3
import socketserver
import sys

import helleh
import tubes


class BankHandler(socketserver.BaseRequestHandler):
    def handle(self):
        tube = tubes.LineTube(self.request)
        cipher = negotiate_helleh(tube)
        message = cipher.decrypt(tube.recv()).decode()
        print(message)


def negotiate_helleh(tube):
    base = helleh.generate_base()
    private, public = helleh.generate_key(base)
    tube.send(helleh.dumps(base))
    tube.send(helleh.dumps(public))
    return helleh.make_shared_cipher(private, helleh.loads(tube.recv()))


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    host, port = sys.argv[1], int(sys.argv[2])
    with ThreadedServer((host, port), BankHandler) as server:
        server.allow_reuse_address = True
        server.serve_forever()


if __name__ == "__main__":
    main()
