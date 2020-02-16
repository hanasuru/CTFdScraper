import rahasia
import time

bendera = rahasia.bendera
m = int(bendera.encode('hex'), 16)
n = rahasia.n
t = int(time.time())
c = pow(m, pow(17, t), n)

print '[*] c: {}\n[*] t: {}\n[*] n: {}'.format(c, t, n)