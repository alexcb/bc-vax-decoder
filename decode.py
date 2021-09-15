data = open('data', 'rb').read().decode('ascii').strip()

import base64
import json
import zlib

from pprint import pprint

def base64_decode(s):
    missing_padding = len(s) % 4
    if missing_padding:
        s += "="* (4 - missing_padding)
    return base64.urlsafe_b64decode(s)

def decode(data):
    data = data.split('/')[1]
    s = []
    for i in range(0, len(data), 2):
        code = data[i:i+2]
        ch = chr(int(code)+45)
        s.append(ch)
    s = ''.join(s)
    parts = [base64_decode(x) for x in s.split('.')]
    header = json.loads(parts[0].decode('utf8'))
    shc_data = zlib.decompress(parts[1], wbits=-15)
    shc_data = json.loads(shc_data.decode('utf8'))

    return header, shc_data, parts[2:]

header, payload, other = decode(data)
pprint(header)
pprint(payload)
pprint(other)

from cryptography.hazmat.primitives.asymmetric import ec, padding
x = base64_decode("xscSbZemoTx1qFzFo-j9VSnvAXdv9K-3DchzJvNnwrY")
y = base64_decode("jA5uS5bz8R2nxf_TU-0ZmXq6CKWZhAG1Y4icAx8a9CA")
assert len(x) == len(y) == 32

public_numbers = ec.EllipticCurvePublicNumbers(
                x=int.from_bytes(x, byteorder="big"),
                y=int.from_bytes(y, byteorder="big"),
                curve=ec.SECP256R1(),
            )
key = public_numbers.public_key()
key.verify('abc', 'foo')
