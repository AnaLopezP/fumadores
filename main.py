import os

from storage import codes, store

def get_puerto(): #Defino el puerto
    while True:
        try:
            puerto = int(input('Puerto (1024 - 49151): '))
            if puerto >= 1024 and puerto <= 49151:
                break
        except Exception:
            pass
    return puerto

#CODIGO PRINCIPAL
if __name__ == '__main__':
    os.system('clear')
    while True:
        print('1. Proveedor')
        print('2. Fumador (5 opciones)')
        type = input('Opcion: ')
        if type in ['1', '2']:
            break
        else:
            os.system('clear')
    os.system('clear')
    if type == '1':
        print('Proveedor')
        from proveedor import init
        init(get_puerto())
    else:
        while True:
            print('Fumador')
            for i in codes:
                print('{}. {}'.format(i, store[i].get('name')))
            type = input('Opcion: ')
            if type in codes:
                break
            else:
                os.system('clear')
        ip = input('IP del proveedor: ')
        from fumador import init
        init(ip, get_puerto(), type)