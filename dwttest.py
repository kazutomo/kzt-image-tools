#!/usr/bin/env python3

import numpy as np
import pywt


orig = np.random.rand(8,8).astype(np.float32)
#print(orig)

co1d = np.full_like(orig, 0)
co1d1d = np.full_like(orig, 0)

for i in range(orig.shape[0]):
    inp = orig[i,:]
    (a, b) = pywt.dwt(inp, 'haar')
    ab = np.concatenate((a,b))
    co1d[i,:] = ab

for i in range(orig.shape[1]):
    inp = co1d[:,i]
    (a, b) = pywt.dwt(inp, 'haar')
    ab = np.concatenate((a,b))
    co1d1d[:,i] = ab

(rows, cols) = co1d1d.shape
rh = rows//2
ch = cols//2
oa = co1d1d[0:rh,    0:ch]
ob = co1d1d[rh:rows, 0:ch]
oc = co1d1d[0:rh,    ch:cols]
od = co1d1d[rh:rows, ch:cols]
    
co2d = pywt.dwt2(orig, 'haar')
a, (b, c, d) = co2d

print('err:a')
print(oa-a)
print('err:b')
print(ob-b)
print('err:c')
print(oc-c)
print('err:d')
print(od-d)


#print('c')
#print(c)
#print('d')
#print(d)
