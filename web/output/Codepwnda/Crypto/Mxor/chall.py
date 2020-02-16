import base64, string

def xors(msg, key):
	res = ''
	for i in range(len(msg)):
		res += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
	return res

flag = open('flag').read()
key = open('key').read()
assert len(key) == 5 and all(x in string.lowercase for x in key)

m = str(int(flag.encode('hex'), 16))
c = xors(m, key)
print base64.b64encode(c)
