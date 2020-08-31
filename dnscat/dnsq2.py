import socket, os, sys, socket, select, time, collections#, threading, random

dns_blacklist = {'8.8.8.8', '8.8.4.4'} if '--no-blacklist' not in sys.argv else set()

resolv_conf = ['/var/run/dnsmasq/resolv.conf', '/run/dnsmasq/resolv.conf', '/etc/resolv.dnsmasq', '/etc/resolv.conf']

def _get_nameservers():
    resolvconf = None
    for i in resolv_conf:
        try: resolvconf = open(i)
        except IOError: pass
        else:
            with resolvconf as file:
                cnt = 0
                for line in file:
                    if line.startswith('nameserver '):
                        yield line[10:].strip()
                        cnt += 1
                if cnt: return

if sys.platform == 'win32':
    from win32ns import get_nameservers as _get_nameservers

def get_nameservers():
    if 'NAMESERVERS' in os.environ: return os.environ['NAMESERVERS'].split(',')
    return _get_nameservers()

def encode_hostname(hostname):
    return b''.join(bytes((len(i),))+i for i in hostname.encode('ascii').split(b'.'))

def encode_query(hostname, record_type):
    return os.urandom(2) + b'\x01 \x00\x01\x00\x00\x00\x00\x00\x01' + encode_hostname(hostname) + b'\x00\x00' + bytes((record_type,)) + b'\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'

def decode_response(q):
    idx = 12
    host = ''
    while True:
        l = q[idx]
        if not l: break
        host += q[idx+1:idx+l+1].decode('ascii') + '.'
        idx += l + 1
    host = host[:-1]
    record_type = q[idx+2]
    idx += 5
    ans = []
    for i in range(int.from_bytes(q[6:8], 'big')):
        l = int.from_bytes(q[idx+10:idx+12], 'big')
        ans.append((int.from_bytes(q[idx:idx+2], 'big'), int.from_bytes(q[idx+2:idx+4], 'big'), q[idx+12:idx+12+l]))
        idx += 12 + l
    return (host, record_type, ans)

def parse_a(ans):
    return [socket.inet_ntoa(i[2]) for i in ans if i[1] == 1]

def parse_txt(data):
    ans = []
    for i in data:
        if i[1] != 16: continue
        i = i[2]
        j = 0
        while j < len(i):
            l = i[j]
            ans.append(i[j+1:j+1+l])
            j += 1 + l
    return ans

def parse_cname(pkt, data):
    ans = []
    for i in data:
        if i[1] != 5: continue
        s = ''
        j = pkt.find(i[2])
        i = pkt
        l = -1
        while l:
            l = i[j]
            if l & 0xc0:
                j = ((l << 8) | i[j + 1]) & 0x3fff
                continue
            s += i[j+1:j+l+1].decode('ascii')+'.'
            j += l + 1
        ans.append(s[:-2])
    return ans

def parse_mx(pkt, data):
    data = [i for i in data if i[1] == 15]
    return list(zip((int.from_bytes(i[2][:2], 'big') for i in data), parse_cname(pkt, ((i[0], 5, i[2][2:]) for i in data))))

DIG_A = 1
DIG_CNAME = 5
DIG_MX = 15
DIG_TXT = 16

class QueryFailed(Exception): pass

class Digger:
    def __init__(self, nameservers=None):
        if nameservers == None: nameservers == get_nameservers()
        self.nameservers = nameservers if nameservers != None else list(get_nameservers())
        self.sockets = []
        self.query_list = collections.OrderedDict()
        self.reopen_sockets()
    def reopen_sockets(self):
        while self.sockets: self.sockets.pop().close()
        for i in self.nameservers:
            sock = socket.socket(socket.AF_INET if ':' not in i else socket.AF_INET6, socket.SOCK_DGRAM)
            while True:
                try: sock.connect((i, 53))
                except socket.error:
                    print('network error, retrying...')
                    time.sleep(1)
                else: break
            self.sockets.append(sock)
        self.queries = 0
        self.query_list.clear()
    def send(self, hostname, record_type):
        sock = self.sockets.pop()
        #threading.Timer(random.random(), sock.send, (encode_query(hostname, record_type),)).start()
        sock.send(encode_query(hostname, record_type))
        self.sockets.insert(0, sock)
        self.queries += 1
        self.query_list[(hostname, record_type)] = time.time()
    def recv(self, timeout=5):
        if self.queries <= 0: return None
        if next(iter(self.query_list.values())) + timeout < time.time():
            k = next(iter(self.query_list))
            h, r = k
            self.query_list.pop(k)
            raise QueryFailed(h, r)
        r, w, x = select.select(self.sockets, [], [], timeout)
        if not r:
            self.reopen_sockets()
            return None
        ans = decode_response(r.pop().recv(1048576))
        del self.query_list[ans[:2]]
        self.queries -= 1
        return ans
