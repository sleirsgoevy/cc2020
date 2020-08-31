from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from sympy.combinatorics.permutations import Permutation
from sympy import factorial
import binascii
import hashlib
import json
import math
import random

LENGTH = 35


def loads(s):
    return Permutation(json.loads(s))


def dumps(perm):
    return json.dumps(list(perm))


def generate_base():
    return Permutation.random(LENGTH)


def generate_key(base):
    private = random.SystemRandom().randint(1, factorial(LENGTH) - 1)
    public = base ** private
    return private, public


def make_shared_cipher(private, public):
    return Cipher(public ** private)


class Cipher:
    def __init__(self, key):
        key = hashlib.sha256(dumps(key).encode()).digest()
        self.__aes = AES.new(key, AES.MODE_CBC, b"\0" * 16)

    def encrypt(self, message):
        return binascii.hexlify(self.__aes.encrypt(pad(message.encode(), 16))).decode()

    def decrypt(self, message):
        return unpad(self.__aes.decrypt(binascii.unhexlify(message)), 16)
