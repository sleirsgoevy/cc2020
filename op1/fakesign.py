import sys

data = open(sys.argv[1], 'rb').read()
assert data[:6] == b'POSO\1\0' and int.from_bytes(data[6:8], 'little') == len(data)
sign_offset = int.from_bytes(data[8:12], 'little')
assert sign_offset == len(data) - 16

def i32(offset):
    return int.from_bytes(data[offset:offset+4], 'little')

var0 = i32(0) ^ i32(0x14)
var4 = i32(4) ^ i32(0x18)
var8 = i32(8) ^ i32(0x1c)
var12 = i32(0xc) ^ i32(0x10)

cx = len(data) - 48
dx = 32

while True:
    var0 ^= i32(dx+4)
    var4 ^= i32(dx+8)
    var8 ^= i32(dx+12)
    var12 ^= i32(dx)
    if cx <= 16: break
    cx -= 16
    dx += 16

a = int.from_bytes(b'CC{r', 'little') ^ var4
b = int.from_bytes(b'1gh7', 'little') ^ var12
c = int.from_bytes(b'w4y}', 'little') ^ var0

data = data[:sign_offset]

data += b'SIGN'
data += a.to_bytes(4, 'little')
data += b.to_bytes(4, 'little')
data += c.to_bytes(4, 'little')

with open(sys.argv[1]+'.signed', 'wb') as file:
    file.write(data)
