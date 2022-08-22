#!/usr/bin/env python3

import sys, math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

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
    
    print(entropy)
    return entropy

# fakedata set. 32*32 becasue of 10 bits
if True:
    print('No room for compression')
    ret = analyze(np.arange(0, 32*32), maxbit=10)
    if ret != 1.0:
        print('Failed to test ret=',ret)
    print('Full room for compression')
    ret = analyze(np.full(32*32, 2), maxbit=10)
    if ret != 0.0:
        print('Failed to test ret=',ret)


#data = (data * (2**10 - 1) / data.max() + np.random.rand(*data.shape)).astype(np.int32)

dims = data.shape

def tofile(bn, d):
    f = open(bn+'.dat', mode='wb')
    np.asarray(d, dtype=np.float32).tofile(f)
    f.close()

    f = open(bn+'-i.dat', mode='wb')
    np.asarray(d, dtype=np.int16).tofile(f)
    f.close()

    plt.imshow(d)
    plt.savefig(bn+'.png')

    
for n in range(0,3):
    print("[Frame%d]" % n)
    d = data[n]

    tofile('orig', d)
    print(d.max())
    print(math.log(d.max(),2))

    # value scaling
    d = (d * (2**10 - 1) / d.max() + np.random.rand(*d.shape)).astype(np.int32)

    tofile('vscaled', d)
    
    # downsample
    nds = 4
    #    dsw = d.shape[0]//nds
    #    ds = d.reshape(-1, nds, dsw, nds).sum((-1,-3))/nds
    convolved = convolve2d(d, np.ones((nds,nds)), mode='valid')
    ds = convolved[::nds, ::nds]/nds
    
    print(d.shape, d.max())
    print(ds.shape, d.max())

    tofile('dsampled',ds.astype(np.int32))

    
    ds = ds.flatten()
    
    analyze(ds, maxbit = 10)

    dp = np.fromiter(map(lambda v: math.sqrt(v), ds), dtype=np.float32)
    analyze(dp, maxbit = 5)

    tofile('sqrt', dp.reshape(-1,128).astype(np.int32))
