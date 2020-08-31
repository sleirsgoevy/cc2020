def perm_mult(a, b):
    return [b[i] for i in a]

def perm_pow(a, n):
    if n == 0: return list(range(len(a)))
    elif n % 2 == 0:
        b = perm_pow(a, n // 2)
        return perm_mult(b, b)
    else:
        return perm_mult(perm_pow(a, n-1), a)

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

def perm_log(a, b):
    n = len(a)
    indices = [False]*n
    loops = {}
    for i in range(n):
        if not indices[i]:
            loop = []
            idx = i
            while not indices[idx]:
                indices[idx] = True
                loop.append(idx)
                idx = a[idx]
            assert idx == i
            loop.reverse()
            for x, y in enumerate(loop):
                loops[y] = (len(loop), x)
    val = 0
    mod = 1
    for i, j in enumerate(b):
        l1, i1 = loops[i]
        l2, i2 = loops[j]
        assert l1 == l2
        m = (i1 - i2) % l1
        mod, val = chinese_theorem(mod, val, l1, m)
    assert perm_pow(a, val) == b
    return val
