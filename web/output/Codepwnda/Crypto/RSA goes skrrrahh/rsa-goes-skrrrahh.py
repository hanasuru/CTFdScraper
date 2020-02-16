from gmpy2 import *
import os, struct, time

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x%m

def generateN(randomST):
    k1 = mpz_urandomb(randomST, 1024)
    k2 = mpz_urandomb(randomST, 1024)

    p = next_prime(k1)
    q = next_prime(k2)

    if is_prime(p, 50) and is_prime(q, 50):
        return [p, q]

def generateKeys(p, q):
    e = 0x10001
    n = p * q
    phi = (p-1) * (q-1)
    d = modinv(e, phi)
    h = (p+0xdeadbeef) * (q+0xdeadbeef)
    return [e, n, h]

def encryptMsg():
    seed = os.urandom(8)
    randomST = random_state(struct.unpack(">Q", seed)[0])

    p, q = generateN(randomST)
    e, n, h = generateKeys(p, q)

    flag = open("flag").read()
    flag = flag.ljust(64, "\x7e")
    flag = int(flag.encode("hex"), 16)
    encrypted = pow(flag, e, n)

    print "Cipher: {}".format(encrypted)
    print "N: {}".format(n)
    print "Hint: {}".format(h)

if __name__ == "__main__":
    encryptMsg()
