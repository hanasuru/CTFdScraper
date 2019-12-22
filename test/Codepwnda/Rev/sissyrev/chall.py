import sys
from binascii import hexlify

def tukar(blok):
    blokyangtertukar = ""
    penukar = [10, 13, 0, 8, 11, 7, 6, 12, 15, 14, 3, 4, 2, 1, 5, 9]
    for dijit in blok:
        dijitbaru = penukar[int(dijit, 16)]
        blokyangtertukar += hex(dijitbaru)[2:]
    return blokyangtertukar

def pad(pesan):
    kurang = 4-(len(pesan)%4)
    return pesan + kurang * chr(kurang)

def hexpad(blok):
    kosong = 8 - len(blok)
    return kosong * "0" + blok

def mutasi(blok):
    pemutasi = [20, 10, 26, 23, 11, 21, 15, 25, 0, 9, 6, 2, 17, 30, 29, 12, 18, 16, 28, 14, 5, 7, 1, 22, 19, 8, 27, 13, 3, 31, 24, 4]
    blok = int(blok, 16)
    dimutasi = 0
    for i in range(32):
        bit = (blok & (1 << i)) >> i
        dimutasi |= bit << pemutasi[i]
    return hexpad(hex(dimutasi)[2:])

def putar(pesan):
    nomerblok = len(pesan)//8
    pesanyangditukar = ""
    for i in range(nomerblok):
        pesanyangditukar += tukar(pesan[8*i:8*i+8])
    pesanyangdimutasi = ""
    for i in range(nomerblok):
        pesanyangdimutasi += mutasi(pesanyangditukar[8*i:8*i+8])
    return pesanyangdimutasi



if __name__ == "__main__":
    sandi = input("insert password !\n")
    rahasia = "d43caa9527cdf4f1e0480b55667a3f2b2dc499e82b01a2cb91cc13a16aab71b4f09fc1c6"
    pesan = str(hexlify(str.encode(pad(sandi))))
    if "\'" in pesan:
        pesan = pesan[2:-1]
    for i in range(1337):
        pesan = putar(pesan)
    if pesan == rahasia:
        print ("Selamat ini flag buat kamu , codepwnda{%s}"%sandi)
    else:
        print("Wrong")