import os, sys, shlex, time, socket, select

sock = socket.create_connection(('isol8.level-up.2020.tasks.cyberchallenge.ru', 20002))

def readline():
    l = b''
    while not l.endswith(b'\n'): l += sock.recv(1)
    return l[:-1].decode('ascii')

ln = readline()
cmd = readline()
assert cmd.startswith('hashcash ')
token = os.popen(' '.join(map(shlex.quote, cmd.split()))).read().strip()
sock.sendall((token+'\n').encode('ascii'))

elf = open(sys.argv[1], 'rb').read()
try: sock.sendall(len(elf).to_bytes(4, 'little')+elf)
except: pass

for i in range(6): print(readline(), file=sys.stderr)

while True:
    r, _, _ = select.select([sock, sys.stdin], [], [])
    if sock in r:
        chk = sock.recv(4096)
        sys.stdout.buffer.raw.write(chk)
        if not chk: break
    if sys.stdin in r: sock.send(sys.stdin.buffer.raw.read(1))
