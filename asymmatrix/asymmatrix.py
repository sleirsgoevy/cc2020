#!/usr/bin/env python3
import numpy as np
import json
import base64

N, M = 2 ** 6 - 2, 10**3 + 7
#N, M = 3, 35
CHALLENGES = 3


def generate_random():
    return np.random.randint(M, size=(N, N))


def spoil(a):
    a = np.copy(a)
    for i in range(0, N // 2):
        r = np.random.randint(M)
        for j in range(N):
            a[i + N // 2, j] = a[i + N // 2, j] + a[i, j] * r
    return a


def mod(a):
    return np.vectorize(lambda x: x % M)(a)


def generate_keypair():
    private_key, a, b = (generate_random() for _ in range(3))
    p, q = (mod(spoil(x)) for x in (a, b))
    private_key = mod(private_key)
    t = mod(-p @ private_key @ private_key - q @ private_key)
    return private_key, (p, q, t)


def encrypt(message, public_key):
    p, q, t = public_key
    r = generate_random()
    return mod(r @ p), mod(r @ q), mod(r @ t + message)


def decrypt(ciphertext, private_key):
    p, q, t = ciphertext
    return mod(t + p @ private_key @ private_key + q @ private_key)


def to_plain(m):
    if type(m) == tuple:
        return {"tuple": [to_plain(x) for x in m]}
    return m.tolist()


def from_plain(p):
    if type(p) == dict:
        return tuple(from_plain(x) for x in p["tuple"])
    return np.array(p)


def dumps(m):
    return json.dumps(to_plain(m))


def loads(s):
    return from_plain(json.loads(s))


def main():
    private, public = generate_keypair()

    print("Hello! My public key:")
    print(dumps(public))

    print("Let's go! First, prove that you're qualified enough:")

    plain = decrypt(loads(input()), private)
    print(plain)
    for i in range(N):
        for j in range(N):
            if plain[i, j] != i + j:
                print("Nope.")
                return

    print("Ok, now it's time for a challenge!")

    for _ in range(CHALLENGES):
        challenge = generate_random()
        encrypted = encrypt(challenge, public)
        print("Please decrypt:")
        print(dumps(encrypted))
        answer = loads(input())
        if not np.array_equal(answer, challenge):
            print("Nope.")
            return

    print("Good job! Here's your reward:")

    with open("flag.txt") as f:
        print(f.read())

    print("Bye!")


if __name__ == "__main__":
    main()
