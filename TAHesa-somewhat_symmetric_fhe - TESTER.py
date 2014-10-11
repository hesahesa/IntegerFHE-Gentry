#function mod symmetric

from __future__ import division
from time import clock
import math

def quot(z, p):
        # http://stackoverflow.com/questions/3950372/round-with-integer-division
        return (z + p // 2) // p
        
def mod(z, p):
        return z - quot(z,p) * p
	

#normal symmetric scheme

import random

LAMBDA = 16 #security parameter
N = LAMBDA
P = LAMBDA ** 2
Q = LAMBDA ** 5

def keygen():
	key = random.getrandbits(P)
	while(key % 2 == 0):
		key = random.getrandbits(P)
	return key

def encrypt(key, aBit):
	q = random.getrandbits(Q)
	m_a = 2 * random.getrandbits(N - 1)
	c = key * q + m_a + aBit
	return c

def decrypt(key, cipherText):
	return mod(cipherText, key) % 2

def add(cipherText1, cipherText2):
	return cipherText1 + cipherText2

def mult(cipherText1, cipherText2):
	return cipherText1 * cipherText2

def tester():
        time_keygen = clock()
        key = keygen()
        print "waktu keygen ", clock() - time_keygen

        m1 = random.getrandbits(1)
        m2 = random.getrandbits(1)
        print "m1 = ", m1
        print "m2 = ", m2

        time_encrypt = clock()
        c1 = encrypt(key, m1)
        print "waktu encrypt ", clock() - time_encrypt
        print "c1 adalah integer sepanjang ", int(math.log10(abs(c1)))+1, " digit"

        c2 = encrypt(key, m2)
        print "c2 adalah integer sepanjang ", int(math.log10(abs(c2)))+1, " digit"

        time_dec = clock()
        decrypt(key, c1)
        print "mm = ", mm
        print "waktu dec ", clock() - time_dec

        time_add = clock()
        c_add = add(c1, c2)
        print "waktu add ", clock() - time_add
        print "c_add adalah integer sepanjang ", int(math.log10(abs(c_add)))+1, " digit"

        time_mult = clock()
        c_mult = mult(c1, c2)
        print "waktu mult ", clock() - time_mult
        print "c_mult adalah integer sepanjang ", int(math.log10(abs(c_mult)))+1, " digit"

        time_dec1 = clock()
        p_add = decrypt(key, c_add)
        print "waktu dec1 ", clock() - time_dec1

        time_dec2 = clock()
        p_mult = decrypt(key, c_mult)
        print "waktu dec2 ", clock() - time_dec2

        print "m1 + m2", p_add
        print "m1 * m2", p_mult
