MOD = 0x3fffffffffffffffffffffffffffffffb

def poly1305(key, message):
    r = int.from_bytes(key[:16], 'little') & 0x0ffffffc0ffffffc0ffffffc0fffffff
    s = int.from_bytes(key[16:], 'little')
    a = 0
    for i in range(0, len(message), 16):
        i = int.from_bytes(message[i:i+16] + b'\1', 'little')
        a = ((a + i) * r) % MOD
    return ((a + s) % 0x100000000000000000000000000000000).to_bytes(16, 'little')

def mod_inv(x):
    # k*x + y*n = 1
    a = x
    b = MOD
    aa = 1
    ab = 0
    ba = 0
    bb = 1
    while a:
        a, aa, ab, b, ba, bb = b, ba, bb, a, aa, ab
        q = a // b
        a -= q * b
        aa -= q * ba
        ab -= q * bb
    assert b == x * ba + MOD * bb == 1
    assert (x * ba) % MOD == 1
    return ba % MOD

def mat_inv(x):
    y = [j[:]+[0]*i+[1]+[0]*(len(j)-i-1) for i, j in enumerate(x)]
    for i in range(len(y)):
        if not y[i][i]:
            for j in range(i+1, len(y)):
                if y[j][i]:
                    y[i], y[j] = y[j], y[i]
                    break
            else: assert False
        for j in range(i+1, len(y)):
            q = (y[j][i] * mod_inv(y[i][i])) % MOD
            for k in range(len(y[j])):
                y[j][k] = (y[j][k] - q * y[i][k]) % MOD
    for i in range(len(y)-1, -1, -1):
        for j in range(i-1, -1, -1):
            q = (y[j][i] * mod_inv(y[i][i])) % MOD
            for k in range(len(y[j])):
                y[j][k] = (y[j][k] - q * y[i][k]) % MOD
    for i in range(len(y)):
        q = mod_inv(y[i][i])
        for j in range(len(y[i])): y[i][j] = (y[i][j] * q) % MOD
    return [i[len(i)//2:] for i in y]

def mat_apply(a, x):
    return [sum((i*j)%MOD for i, j in zip(l, x))%MOD for l in a]

def get_matrix(k):
    mat = [[int.from_bytes(i[:16]+b'\1', 'little'), int.from_bytes(i[16:]+b'\1', 'little'), 1, 0] for i in k]
    mat[3][3] = 1
    return mat_inv(mat)

def solve_gen(k, v):
    v = [int.from_bytes(i, 'little') for i in v]
    assert len(k) == len(v) == 4
    m = get_matrix(k)
    for mask in range(256):
        v1 = v[0] | (mask & 192) << 122
        v2 = v[1] | (mask & 48) << 124
        v3 = v[2] | (mask & 12) << 126
        v4 = v[3] | (mask & 3) << 128
        if max(v1, v2, v3, v4) >= MOD:
            continue
        vv = mat_apply(m, [v1, v2, v3, v4])
        if vv[3] or vv[0] != (vv[1] * vv[1]) % MOD or vv[2] >= 0x100000000000000000000000000000000:
            continue
        yield vv[1].to_bytes(16, 'little')+vv[2].to_bytes(16, 'little')

def solve(k, v):
    return list(solve_gen(k, v))

if __name__ == '__main__':
    pairs = [list(map(bytes.fromhex, input().split())) for i in range(4)]
    k, v = zip(*pairs)
    print(list(map(bytes.hex, solve_gen(k, v))))
