class LineTube:
    def __init__(self, sock):
        self.__sock = sock

    def send(self, s):
        self.__sock.send(s.encode() + b"\n")

    def recv(self):
        s = b""
        while not s.endswith(b"\n"):
            s += self.__sock.recv(1)
        s = s[:-1].decode()
        return s
