import subprocess, sys

x = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def xchg(data):
    assert len(data) == 184
    while data: data = data[x.stdin.write(data):]
    x.stdin.flush()
    data = b''
    while len(data) < 184: data += x.stdout.read(184 - len(data))
    return data

syscalls = {i[1][5:]: int(i[2]) for i in map(str.split, open('/usr/include/x86_64-linux-gnu/asm/unistd_64.h')) if len(i) == 3 and i[0] == '#define' and i[1].startswith('__NR_') and i[2].isnumeric()}

while True:
    spec = input()
    args = spec.split(' ', 7)
    blob = args.pop()
    while len(args) < 7: args.append('0')
    args = [int(i, 0) for i in args[1:]] + [syscalls[args[0]]]
    data = b''.join((i & ((1 << 64) - 1)).to_bytes(8, 'little') for i in args) + eval(blob)
    assert len(data) < 184
    data = xchg(data + bytes(184 - len(data)))[:len(data)]
    print(int.from_bytes(data[48:56], 'little', signed=True), data[56:])
