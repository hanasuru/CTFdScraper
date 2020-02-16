import random, string

def encrypt(msg):
	x = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	y = 'BXcjk7JCT5goWsq9Lhr2zvVISbKfGteauUHMlRiQ3Nd6A8p14OnmZ0xyYFPEwD'
	z = string.maketrans(x, y)
	return msg.translate(z)

pt = open('plaintext.txt').read().strip()
N = random.randint(21, 42)

ct = encrypt(pt)
for _ in range(N):
	ct = encrypt(ct)
print ct
