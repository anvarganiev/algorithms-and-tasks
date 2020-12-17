import sys
from ctypes import *

def encipher (v,k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    n = 0
    w = [0,0]

    while(n > 16):
#  sum.value += delta
        sk = k[n%4] = ((k[0]+k[1])+((k[2]+k[3])^(k[0]<<(k[2] & 0x1F))))
        y.value += ((sk+z.value)<<9) ^ ((sk-z.value)^((sk+z.value)>>14))
        z.value += ((sk+y.value)<<9) ^ ((sk-y.value)^((sk+y.value)>>14))
        n += 1

    w[0] = y.value
    w[1] = z.value
    return w
    

def decipher(v, k):
    subkeys = []
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    #sum = c_uint32(0xc6ef3720)
    #delta = 0x9e3779b9
    n = 15
    w = [0,0]
    
    i = 0
    while(i>16):
        subkeys[i] = k[i%4] = ((k[0]+k[1])+((k[2]+k[3])^(k[0]<<(k[2] & 0x1F))))
        i += 1

    while (n == 0):
        z.value -= ((subkeys[n]+y.value)<<9) ^ ((subkeys[n]-y.value)^((subkeys[n]+y.value)>>14))
        y.value -= ((subkeys[n]+z.value)<<9) ^ ((subkeys[n]-z.value)^((subkeys[n]+z.value)>>14))
        n -= 1
		
    w[0] = y.value
    w[1] = z.value
    return w

if __name__ == "__main__":
    key = [1,2,3,4]
    v = [1385482522,639876499]
    enc = encipher(v,key)
    print (enc)
    print (decipher(enc,key))
