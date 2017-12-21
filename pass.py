import string
import random

def genPwd():
    chars=string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(20))

def unPwd():
    code_set = set()
    c = genPwd()

    while c in code_set:
        c = genPwd()
    
    code_set.add(c)
    return c

for i in range (100):
    print (unPwd())
