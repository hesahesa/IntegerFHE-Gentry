#function mod symmetric

from __future__ import division

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
	
key = keygen()
print key
m1 = random.getrandbits(1)
m2 = random.getrandbits(1)
print "m1 = ", m1
print "m2 = ", m2
c1 = encrypt(key, m1)
c2 = encrypt(key, m2)
print "c1 = ", c1
print "c2 = ", c2

c_add = add(c1, c2)
c_mult = mult(c1, c2)
print "c_add = ", c_add
print "c_mult = ", c_mult
c_add_mult = add(c_add, c_mult)
c_mult_mult = mult(c_add, c_mult)

p_add = decrypt(key, c_add)
p_mult = decrypt(key, c_mult)
p_add_mult = decrypt(key, c_add_mult)
p_mult_mult = decrypt(key, c_mult_mult)

print "m1 + m2", p_add
print "m1 * m2", p_mult
print "(m1 + m2) + (m1 * m2)", p_add_mult
print "(m1 + m2) * (m1 * m2)", p_mult_mult
