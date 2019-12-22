import random
import hashlib
def menu():
    banner ='''          
             _/                  _/           
    _/_/_/  _/_/_/      _/_/_/      _/_/_/    
 _/        _/    _/  _/    _/  _/  _/    _/   
_/        _/    _/  _/    _/  _/  _/    _/    
 _/_/_//_//    _/    _/_/_/  _/  _/    _/     
   _/      _/    _/  _/_/_/      _/_/_/       
_/_/_/_/  _/    _/  _/    _/  _/              
 _/      _/    _/  _/    _/  _/               
_/        _/_/_/  _/    _/    _/_/_/                                                   
    '''
    print banner
def opt():
    option = '''option     :
[1] encrypt-message
[2] check-flag
[3] ex-it
    '''
    print option
    a = raw_input('choose     : ')
    if a=='1':
        print encrypt(raw_input('plaintext  : '))
        opt()
    elif a=='2':
        print check(raw_input("input flag : "))
        exit()
    else:
        exit()




def f0(x):
    a = 0
    b = 1
    while(x):
        a = a + b
        b = a - b
        x = x - 1
    return (a+b)%10

def f1(x):
    a = ""
    for i in range(len(x)):
        a += chr((ord(x[i])^f0(i))%256)
    return a

def f2(x):
    q, r, t, k, n, l, y = 1, 0, 1, 1, 3, 3, []
    while (len(y)<len(x)):
        if 4*q+r-t < n*t:
            y.append(n)
            nr = 10*(r-n*t)
            n  = ((10*(3*q+r))//t)-10*n
            q  *= 10
            r  = nr
        else:
            nr = (2*q+r)*l
            nn = (q*(7*k)+2+(r*l))//(t*l)
            q  *= k
            t  *= l
            l  += 2
            k += 1
            n  = nn
            r  = nr
    x  = x[::-1]
    z  = [chr(ord(x[i])-y[i]%256) for i in range(0,len(x),2)]
    v  = [chr((ord(x[i])+y[i])%256) for i in range(1,len(x),2)]
    v += z
    return v

def f3(x,z):
    y = []
    while x != 1:
        y.append(x%z)
        if x % 2 == 0:
            x = int(x/2)
        else:
            x = int(3*x+1)
    else:
        y.append(x%z)
        if len(y)&1:
            return y[1:]
        else :
            return y

def f4(x,y):
    a = x[:len(x)/2]
    b = x[len(x)/2:]
    for i in range(len(a)):
        z       = y[a[i]]
        y[a[i]] = y[b[i]]
        y[b[i]] = z
    z = [chr(i) for i in y]
    return "".join(z)

def encrypt(x):
    key = random.randint(1337,7331)
    x = f2(f1(x))
    y = [ord(i) for i in x]
    return 'encrypted  : '+ f4(f3(key,len(x)),y).encode("hex")

def check(x):
  if hashlib.md5(x).hexdigest() == "b4fdeab83ba1cab8db95127657556a40":
    return "Correct, The Flag is : \ncodepwnda{%s}" % x 
  else:
    return "Wrong Flag !"

menu()
opt()
