import dnsq2

for i in open('dnses.txt'):
    pkt = eval(i)
    data = dnsq2.decode_response(pkt)
    if data[0].startswith('dnscat.') and data[2]:
        if data[1] == dnsq2.DIG_CNAME:
            payload = ''.join(i[7:] for i in dnsq2.parse_cname(pkt, data[2]) if i.startswith('dnscat.'))
        elif data[1] == dnsq2.DIG_TXT:
            payload = b''.join(dnsq2.parse_txt(data[2])).decode('ascii')
        elif data[1] == dnsq2.DIG_MX:
            payload = ''.join(i[1][7:] for i in dnsq2.parse_mx(pkt, data[2]) if i[1].startswith('dnscat.'))
        else:
            assert False
        print('o<', bytes.fromhex(data[0][7:].replace('.', '')))
        print('o>', bytes.fromhex(payload.replace('.', '')))
