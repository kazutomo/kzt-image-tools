#!/usr/bin/env python3

import sys, math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import struct

fn = ''

if len(sys.argv) > 1:
    fn = sys.argv[1]

data = np.load(fn)
print('data:', fn)


def analyze(clipped, maxbit = 10):
    hmap = {}
    for v in clipped:
        if v in hmap.keys():
            hmap[v] += 1
        else:
            hmap[v] = 1

    entropy = 0.0
    
    ndata = float(len(clipped))
    nvals = 1<<maxbit
    for k in hmap.keys():
        p = float(hmap[k]) / ndata
        entropy -= p * math.log(p, nvals)
    
    return entropy

# fakedata set. 32*32 becasue of 10 bits
if True:
    print('No room for compression')
    ret = analyze(np.arange(0, 32*32), maxbit=10)
    if ret != 1.0:
        print('Failed to test ret=',ret)
    print(ret)
    print('Full room for compression')
    ret = analyze(np.full(32*32, 2), maxbit=10)
    if ret != 0.0:
        print('Failed to test ret=',ret)
    print(ret)

dims = data.shape

def tofile(bn, d):
    n = len(d)
    duint64 = ds.astype('uint16')
    bd = struct.pack('=%dH' % n, *duint64)
    f = open(bn+'.dat', mode='wb')
    f.write(bd)
    f.close()

    
for n in range(0,1):
    print("[Frame%d]" % n)
    d = data[n]

    print('Max:', d.max(), math.log(d.max(),2))
    
    frombits = 16

    ds = d.flatten()
    ent = analyze(ds, maxbit = frombits)
    print('entropy:', ent)

    tofile('bin%03d'%n, ds)
