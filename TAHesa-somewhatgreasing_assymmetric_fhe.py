#function mod symmetric

from __future__ import division
from decimal import *
import functools
import math
import random
import operator

def quot(z, p):
        # http://stackoverflow.com/questions/3950372/round-with-integer-division
        return (z + p // 2) // p
        
def mod(z, p):
        return z - quot(z,p) * p
        
#normal asymmetric scheme

LAMBDA = 42 #2**3 #security parameter
RHO = 16 #LAMBDA #bit-length of noise
RHO_P = RHO + long(math.ceil(math.log(LAMBDA, 2)))
GAMMA = 160000 #LAMBDA ** 5 #bit-length int in public key
ETA = 1088 #LAMBDA ** 2 #bit-length of secret key
TAU = GAMMA + LAMBDA #number of int in public key
GAMMA_PER_P = 0
#greasing sec param
THETA = 15 #LAMBDA
KAPPA = GAMMA + 2 + long(math.ceil(math.log(THETA + 1, 2))) #GAMMA * ETA // RHO_P
BIG_THETA = 144 #2 * THETA
getcontext().prec = KAPPA + 1
#jumlah bit integer
NUMBITS = 8

def samplingPubKey(p):
        global GAMMA_PER_P
        if(GAMMA_PER_P == 0):
                GAMMA_PER_P = (2**GAMMA)//p
        q = random.randint(0, GAMMA_PER_P - 1)
        r = random.randint(-1 * (2**RHO) + 1, 2**RHO - 1)
        x = p * q + r
        return x

def keygen():
        print "Generating key..."
        sk = random.randint(2**(ETA-1), 2**ETA - 1)
        while(sk % 2 == 0):
                sk = random.randint(2**(ETA-1), 2**ETA - 1)
        pubKeyTmp = samplingPubKey(sk)
        while(not((pubKeyTmp % 2 != 0) and (mod(pubKeyTmp, sk) % 2 == 0))):
                pubKeyTmp = samplingPubKey(sk)
        pk = [pubKeyTmp for x in range(TAU)]
        maxvalpk = max(pk)
        while(not((maxvalpk % 2 != 0) and (mod(maxvalpk, sk) % 2 == 0))):
                pk = [samplingPubKey(sk) for x in range(TAU)]
                maxvalpk = max(pk)
        posmaxpk = pk.index(maxvalpk)
        tmp = pk[posmaxpk]
        pk[posmaxpk] = pk[0]
        pk[0] = tmp
        print "Generating key...[done]"
        return (sk, pk)


def encrypt(publicKey, aBit):
        print "Encrypting..."
        numberElem = random.randint(1, TAU-1)
        subsetKey = random.sample(publicKey[1:], numberElem)
        r = random.randint(-1 * (2**RHO_P) + 1, 2**RHO_P - 1)
        sigmaSubKey = reduce(operator.add, subsetKey)
        c = mod(aBit + 2 * r + 2 * sigmaSubKey, publicKey[0])
        return c
        

def decrypt(secretKey, cipherText):
        print "Decrypting..."
        #m_p = mod(cipherText, secretKey) % 2
        m_p = (cipherText - quot(cipherText, secretKey)) % 2
        return m_p

def add(publicKey, cipherText1, cipherText2):
        return cipherText1 + cipherText2

def mult(publicKey, cipherText1, cipherText2):
        return cipherText1 * cipherText2

def recrypt(pk2,sk1_vec,c1):
        #salah
        c1_bit = [1 if digit=='1' else 0 for digit in bin(c1)[2:]]
        c1_vec = [encrypt(pk2,c1_bit[j]) for j in range(len(c1_bit))]
        c_vec = [decrypt(sk1_vec[j],ci_vec[j]) for j in range(ETA)]
        out = 0
        for bit in c_vec:
                out = (out << 1) | bit
        return out

def convertToBitList(angka):
        bitlist = [1 if digit=='1' else 0 for digit in bin(angka)[2:]]
        bitlist = [0 for x in range(NUMBITS - len(bitlist))] + bitlist
        return bitlist

def convertToInt(bitlist):
        out = 0
        for bit in bitlist:
                out = (out << 1) | bit
        return out

def encryptInt(pk, number):
        bitlist = convertToBitList(number)
        cipherlist = [encrypt(pk,bitlist[i]) for i in range(len(bitlist))]
        return cipherlist

def decryptInt(sk, cipherlist):
        plainlist = [decrypt(sk, cipherlist[i]) for i in range(len(cipherlist))]
        number = convertToInt(plainlist)
        return number

def halfadder(b1, b2):
        jumlah = b1 + b2
        cout = b1 * b2
        return (jumlah, cout)

def fulladder(b1, b2, cin):
        (jumlah1, carry1) = halfadder(b1, b2)
        (jumlah2, carry2) = halfadder(cin, jumlah1)
        cout = (carry1 + carry2) + (carry1 * carry2)
        return (jumlah2, cout)

def jumlahInt(num1, num2):
        #index 0 adalah msb
        #a0, a1, a2, a3, a4, a5, a6, a7, ...
        #b0, b1, b2, b3, b4, b5, b6, b7, ...
        #----------------------------------- +
        #c0, c1, c2, c3, c4, c5, c6, c7, ...
        hasil = [0 for x in range(NUMBITS)]
        carry = 0
        for i in range(NUMBITS-1,-1,-1):
                (jumlah, carry) = fulladder(num1[i],num2[i],carry)
                hasil[i] = jumlah
        return hasil

#greasing scheme

def add_mod(modulus, x, y):
        return mod(x+y, modulus)        

def keygen_s():
        print "Generating key (greasing)..."
        (sk_, pk_) = keygen()
        xp = quot(2**KAPPA, sk_)
        s_vec = [1 for x in range(THETA)] + [0 for x in range(BIG_THETA - THETA)]
        random.shuffle(s_vec)
        #u_vec = [random.randint(0, 2**(KAPPA + 1) - 1) for x in range(BIG_THETA)]

        #cobacoba
        uVecTmp = random.randint(0, 2**(KAPPA + 1) - 1)
        u_vec = [uVecTmp for x in range(BIG_THETA)]
        #end cobacoba


        #start fix pubkey
        print "Fixing pubkey (greasing)..."
        add_mod_partial = functools.partial(add_mod, 2**(KAPPA+1))
        pos_first_1 = s_vec.index(1)
        u_vec_inc = [u_vec[x] for x in range(pos_first_1 + 1, len(u_vec)) if s_vec[x] == 1]    
        sum_pubkey = reduce(add_mod_partial, u_vec_inc)
        u_first = xp - mod(sum_pubkey, 2**(KAPPA+1))
        if (u_first < 0): u_first = u_first * -1
        u_vec[pos_first_1] = u_first
        assert add_mod_partial(sum_pubkey, u_first) == mod(xp, 2**(KAPPA+1)), "fail not equal"
        print "Fixing pubkey (greasing)...[done]"
        #end fix pubkey

        y_vec = [Decimal(u_vec[x]) / Decimal(2**KAPPA) for x in range(BIG_THETA)]
        #output sk, pk
        print "Generating key (greasing)...[done]"
        return (s_vec, (pk_, y_vec))

def encrypt_s(publicKey_s, aBit):
        print "Encrypting (greasing)..."
        (pk_, y_vec) = publicKey_s
        c_ = encrypt(pk_, aBit)
        accuracy = Decimal("10") ** (-1 * long(math.ceil(math.log(THETA, 2)) + 3))
        z_vec = [((c_ * y_vec[i]) % 2).quantize(accuracy) for i in range(BIG_THETA)]
        #output cipher, vector z hasil preprocess
        print "Encrypting (greasing)...[done]"
        return (c_, z_vec)
        
def decrypt_s(secretKey_s, cipherText_s):
        print "Decrypting (greasing)..."
        s_vec = secretKey_s
        (c_, z_vec) = cipherText_s
        z_secret = [z_vec[x] for x in range(BIG_THETA) if s_vec[x] == 1]
        sz_sum = reduce(operator.add, z_secret).to_integral_value(rounding = ROUND_HALF_UP)
        m_p = (c_ - sz_sum) % 2
        m_p = int(m_p) % 2
        print "Decrypting (greasing)...[done]"
        return m_p

def add_s(publicKey_s, cipherText_s1, cipherText_s2):
        (pk_, y_vec) = publicKey_s
        c_ = cipherText_s1[0] + cipherText_s2[0]
        accuracy = Decimal("10") ** (-1 * long(math.ceil(math.log(THETA, 2)) + 3))
        z_vec = [((c_ * y_vec[i]) % 2).quantize(accuracy) for i in range(BIG_THETA)]
        return (c_, z_vec)

def mult_s(publicKey_s, cipherText_s1, cipherText_s2):
        (pk_, y_vec) = publicKey_s
        c_ = cipherText_s1[0] * cipherText_s2[0]
        accuracy = Decimal("10") ** (-1 * long(math.ceil(math.log(THETA, 2)) + 3))
        z_vec = [((c_ * y_vec[i]) % 2).quantize(accuracy) for i in range(BIG_THETA)]
        return (c_, z_vec)

def tesgreasing():
        (sk, pk) = keygen_s()
        m1 = 1
        m2 = 1
        print "m1 = ", m1
        print "m2 = ", m2
        c1 = encrypt_s(pk, m1)
        c2 = encrypt_s(pk, m2)
        mm1 = decrypt_s(sk, c1)
        mm2 = decrypt_s(sk, c2)
        print "mm1 = ", mm1
        print "mm2 = ", mm2

        c_add = add_s(pk, c1, c2)
        c_mult = mult_s(pk, c1, c2)
        #print "c_add = ", c_add
        #print "c_mult = ", c_mult

        p_add = decrypt_s(sk, c_add)
        p_mult = decrypt_s(sk, c_mult)

        print "m1 + m2", p_add
        print "m1 * m2", p_mult

def tesnormal():
        (sk, pk) = keygen()
        m1 = 1
        m2 = 1
        print "m1 = ", m1
        print "m2 = ", m2
        c1 = encrypt(pk, m1)
        c2 = encrypt(pk, m2)
        mm1 = decrypt(sk, c1)
        mm2 = decrypt(sk, c2)
        print "mm1 = ", mm1
        print "mm2 = ", mm2

        c_add = add(pk, c1, c2)
        c_mult = mult(pk, c1, c2)
        #print "c_add = ", c_add
        #print "c_mult = ", c_mult

        p_add = decrypt(sk, c_add)
        p_mult = decrypt(sk, c_mult)

        print "m1 + m2", p_add
        print "m1 * m2", p_mult

def tesint():
        (sk, pk) = keygen()
        angka1 = 100
        angka2 = 70
        c1 = encryptInt(pk, angka1)
        c2 = encryptInt(pk, angka2)
        print "---angka1 = ", decryptInt(sk, c1)
        print "---angka2 = ", decryptInt(sk, c2)
        jumlah = jumlahInt(c1, c2)
        print "---total = ", decryptInt(sk, jumlah)

