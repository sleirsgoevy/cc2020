#!/usr/bin/env python3
import socketserver
import sys

import diffid
import tubes


class BankHandler(socketserver.BaseRequestHandler):
    def handle(self):
        tube = tubes.LineTube(self.request)
        cipher = negotiate_diffid(tube)
        message = cipher.decrypt(tube.recv()).decode()
        print(message)


def negotiate_diffid(tube):
    base = diffid.generate_base()
    private, public = diffid.generate_key(base)
    tube.send(diffid.dumps(base))
    tube.send(diffid.dumps(public))
    return diffid.make_shared_cipher(private, diffid.loads(tube.recv()))


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    host, port = sys.argv[1], int(sys.argv[2])
    with ThreadedServer((host, port), BankHandler) as server:
        server.allow_reuse_address = True
        server.serve_forever()


if __name__ == "__main__":
    main()
