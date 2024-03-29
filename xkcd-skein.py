#!/usr/bin/env python3

import skein
from random import shuffle
from multiprocessing import Pool

TARGET = "5b4da95f5fa08280fc9879df44f418c8f9f12ba424b7757de02bbdfbae0d4c4fdf9317c80cc5fe04c6429073466cf29706b8c25999ddd2f6540d4475cc977b87f4757be023f19b8f4035d7722886b78869826de916a79cf9c94cc79cd4347d24b567aa3e2390a573a373a48a5e676640c79cc70197e1c5e7f902fb53ca1858b6"

def bitdiff(a0, b0):
    a1 = bytes.fromhex(a0)
    b1 = bytes.fromhex(b0)

    wrong = []
    for n in range(0, len(a1)):
        wrong.append(a1[n] ^ b1[n])

    wrong_total = 0
    for byte in wrong: # for each byte
        for off in range(0, 8): # for each bit
            if byte >> off & 0x01:
                wrong_total = wrong_total + 1
    return wrong_total


def tryval(n):
    h = skein.skein1024(bytes(n, "utf8"), digest_bits=1024).hexdigest()
    d = bitdiff(h, TARGET)
    #if n % 100000 == 0:
    #    print(n)
    if d < 425:
        print(n, d)


#x = 5
#v = 10000000
#vals = range(x * v, (x + 1) * v)

vals = [
    n.strip()
    for n in open("/usr/share/dict/words").readlines()
    if n[0] >= 'a' and n[0] <= 'z' and "'" not in n and len(n) > 3
]

print(len(vals), "inputs")

shuffle(vals)


p = Pool(4)
for v in vals[4:]:
    for w in vals:
        for x in vals:
            p.map(tryval, [" ".join([v, w, x, y]) for y in vals], 1000)

