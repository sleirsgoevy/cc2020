import socket, sys, asymmatrix, json, numpy

def mod_inv(x, mod):
    # k*x + y*n = 1
    a = x
    b = mod
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
    assert b == x * ba + mod * bb == 1
    assert (x * ba) % mod == 1
    return ba % mod

def mat_inv(x, mod):
    y = [j[:]+[0]*i+[1]+[0]*(len(j)-i-1) for i, j in enumerate(x)]
    for i in range(len(y)):
        if not y[i][i]:
            for j in range(i+1, len(y)):
                if y[j][i]:
                    y[i], y[j] = y[j], y[i]
                    break
            else: assert False
        for j in range(i+1, len(y)):
            q = (y[j][i] * mod_inv(y[i][i], mod)) % mod
            for k in range(len(y[j])):
                y[j][k] = (y[j][k] - q * y[i][k]) % mod
    for i in range(len(y)-1, -1, -1):
        for j in range(i-1, -1, -1):
            q = (y[j][i] * mod_inv(y[i][i], mod)) % mod
            for k in range(len(y[j])):
                y[j][k] = (y[j][k] - q * y[i][k]) % mod
    for i in range(len(y)):
        q = mod_inv(y[i][i], mod)
        for j in range(len(y[i])): y[i][j] = (y[i][j] * q) % mod
    return [i[len(i)//2:] for i in y]

def mat_apply(a, x, mod):
    return [sum((i*j)%mod for i, j in zip(l, x))%mod for l in a]

def solve1(a, b, mod):
    a = [[j % mod for j in i] for i in a]
    b = [i % mod for i in b]
    a1 = mat_inv(a, mod)
    return mat_apply(a1, b, mod)

def chinese_theorem(n, x, m, y):
    # k * n + x == l * m + y
    # k * n - l * m = y - x
    a = n
    b = m
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
    assert ba * n + bb * m == b
    assert (y - x) % b == 0
    q = (y - x) // b
    k = ba * q
    l = -bb * q
    val = k * n + x
    assert val == l * m + y
    mod = n * m // b
    assert mod % n == mod % m == 0
    val %= mod
    assert val % n == x and val % m == y
    return (mod, val)

def solve2(a, b, mod1, mod2):
    ans = [chinese_theorem(mod1, i, mod2, j)[1] for i, j in zip(solve1(a, b, mod1), solve1(a, b, mod2))]
    assert mat_apply(a, ans, mod1 * mod2) == b
    return ans

def solve(a, b, mod1, mod2):
    return list(map(list, zip(*(solve2(a, i, mod1, mod2) for i in map(list, zip(*b))))))

def solve_rev(a, b, mod1, mod2):
    return list(map(list, zip(*solve(list(map(list, zip(*a))), list(map(list, zip(*b))), mod1, mod2))))

def main():
    sock = socket.create_connection((sys.argv[1], int(sys.argv[2])))
    def readline():
        ans = b''
        while not ans.endswith(b'\n'): ans += sock.recv(1)
        return ans[:-1].decode('ascii')
    readline()
    pubkey = asymmatrix.from_plain(json.loads(readline()))
    readline()
    msg = numpy.matrix([[i+j for i in range(62)] for j in range(62)])
    sock.sendall((json.dumps(asymmatrix.to_plain(asymmatrix.encrypt(msg, pubkey)))+'\n').encode('ascii'))
    while not readline().startswith('Ok'): pass
    print('sanity check passed!')
    for i in range(3):
        readline()
        print('decrypting #%d'%i)
        p, q, t = pubkey
        rp, rq, rt_msg = asymmatrix.from_plain(json.loads(readline()))
        try: r = numpy.matrix(solve_rev(p.tolist(), rp.tolist(), 19, 53))
        except: r = numpy.matrix(solve_rev(q.tolist(), rq.tolist(), 19, 53))
        assert (asymmatrix.mod(r * p) == rp).all() and (asymmatrix.mod(r * q) == rq).all()
        ans = asymmatrix.mod(rt_msg - r * t)
        sock.sendall((json.dumps(asymmatrix.to_plain(ans))+'\n').encode('ascii'))
        print('done!')
    while True: print(readline())

if __name__ == '__main__': main()
