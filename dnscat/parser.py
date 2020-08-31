import dnsq2

for i in open('dnses.txt'):
    pkt = eval(i)
    data = dnsq2.decode_response(pkt)
    if data[1] == dnsq2.DIG_CNAME:
        print(data[0], 'CNAME', dnsq2.parse_cname(pkt, data[2]))
    elif data[1] == dnsq2.DIG_TXT:
        print(data[0], 'TXT', dnsq2.parse_txt(data[2]))
    elif data[1] == dnsq2.DIG_MX:
        print(data[0], 'MX', dnsq2.parse_mx(pkt, data[2]))
    else:
        print(data[0], 'UNKNOWN', data)
