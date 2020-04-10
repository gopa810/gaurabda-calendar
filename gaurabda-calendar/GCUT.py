def val(a,b,msg):
    if a!=b:
        print(f'{msg} ... Value left: {a}, value right: {b}')
    else:
        print(f'{msg} ... OK')

def nval(a,b,msg):
    if a==b:
        print(f'{msg} ... Value left: {a}, value right: {b}')
    else:
        print(f'{msg} ... OK')

def info(str):
    print(f'--- {str} ---')

def msg(str):
    print(str)
