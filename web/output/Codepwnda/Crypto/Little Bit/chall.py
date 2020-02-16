import base64, random

def pad(msg):
	return msg << (6 - (msg.bit_length() % 6))

def cut(msg):
	res = []
	while msg:
		res.append(msg & (2**6 - 1))
		msg = msg >> 6
	return res

def encrypt(msg):
	msg = pad(int(msg.encode('hex'), 16))
	myBits = cut(msg)
	return ''.join(chr(4*x + random.randint(0, 3)) for x in myBits)

def main():
	pt = open('flag').read()
	ct = encrypt(pt)
	print 'Encrypted flag:', base64.b64encode(ct)

if __name__ == '__main__':
	main()
