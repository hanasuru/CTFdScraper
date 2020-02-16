from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__, template_folder='./templates')
f_f = open('flag.txt', 'r')
f_k = open('key', 'r')
flag = f_f.read()
key = f_k.read()
f_k.close()
f_f.close()

flag_enc = ''
for i, x in enumerate(flag):
	flag_enc += chr(ord(x)^ord(key[i%len(key)]))

@app.route('/')
def index():
	return render_template('index.html', flag_enc=flag_enc.encode('utf-8').hex())

@app.route('/decrypt', methods=['POST'])
def decrypt():
	data = request.get_data().decode("utf-8")
	data = json.loads(data)
	key_in = ''
	
	try:
		for d in data:
			if d['name'] == 'key':
				key_in = d['value']
				break
	except:
		return 'error!'
	
	try:
		if len(key_in) != len(key):
			return 'key salah mank.'
		res = ''
		for i in range(len(flag)):
			k_in, k, f_enc = ord(key_in[i%len(key)]), ord(key[i%len(key)]), ord(flag_enc[i])
			if k_in != k:
				return 'key salah mank.'

			res += chr(k ^ f_enc)
		return res
	except:
		return 'error!'

	return key_in
