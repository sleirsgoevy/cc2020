#!/usr/bin/env python3
import binascii
import json
import socket
import sys

import diffid
import tubes


def main():
    host, port = sys.argv[1], int(sys.argv[2])
    with socket.socket() as sock:
        sock.connect((host, port))
        tube = tubes.LineTube(sock)
        cipher = negotiate_diffid(tube)
        message = json.dumps(input_transaction())
        tube.send(cipher.encrypt(message))


def negotiate_diffid(tube):
    base = diffid.loads(tube.recv())
    private, public = diffid.generate_key(base)
    tube.send(diffid.dumps(public))
    return diffid.make_shared_cipher(private, diffid.loads(tube.recv()))


def input_transaction():
    print("Enter your transaction.\n")
    return {
        "from_account": input("From: "),
        "to_account": input("To: "),
        "amount": int(input("Amount: ")),
        "comment": input("Comment: "),
    }


if __name__ == "__main__":
    main()
