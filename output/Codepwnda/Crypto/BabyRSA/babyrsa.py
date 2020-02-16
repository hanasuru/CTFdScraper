flag = open("flag").read()
m = int(flag.encode("hex"), 0x16)
e = 0x10001
n = 0x54012066b18843995165c3c0d783aa9e31e796f6928ea4bfe0728b1d1bad6271
print pow(m, e, n)
