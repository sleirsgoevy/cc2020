#!/usr/bin/env python3
from chacha20poly1305 import Poly1305
import custom_impl
import os


def mac(key, message):
    a = Poly1305(key).create_tag(message)
    b = custom_impl.poly1305(key, message)
    assert a == b
    return a


def verify(key, message, tag):
    return mac(key, message) == tag


def main():
    key = os.urandom(32)

    for _ in range(32):
        message = os.urandom(32)
        print(message.hex(), mac(key, message).hex())

    challenge = os.urandom(32)
    print(challenge.hex(), "X" * 32)

    for _ in range(32):
        try:
            tag = bytes.fromhex(input("Enter tag: "))
            if verify(key, challenge, tag):
                with open("flag.txt") as f:
                    print(f.read())
                return
        except:
            return
        print("Access denied.")


if __name__ == "__main__":
    main()
