# Fumadores

La dirección de GitHub de este repositorio es la siguiente: 
[GitHub](https://github.com/AnaLopezP/fumadores.git)
https://github.com/AnaLopezP/fumadores.git

# Código: 
Archivo fumador:

```
import socket
import time

from storage import packet_size, store, time_sleep, time_smoke
from utils import _print

def proceso(code, request): #Función que manda los distintos mensajes posibles del fumador al servidor y lo ejecuta.
    mensaje = "" #Mensaje que va cambiando con el que nos comunicamos al servidor
    while True:
        if mensaje != 'ack':
            _print("Esperando {}!".format(store.get(code)['required'])) #Espero por el ingrediente (recurso) requerido
            request.send('need'.encode('UTF-8')) #Envío la petición del recurso al servidor
        
        mensaje = request.recv(packet_size).decode('UTF-8') #Espero por la respuesta del servidor y la almaceno en la variable
        if mensaje == 'enable': #Si el mensaje recibido es enable, es que ya tengo todo para fumar
            _print('¡Servido!')
            time.sleep(time_sleep)
            request.send('ack'.encode('UTF-8'))
            _print('Armando cigarro')
            time.sleep(time_sleep)
            _print('Fumando')
            time.sleep(time_smoke)
            request.send('enable'.encode('UTF-8'))

        elif mensaje == 'ack':
            pass
        time.sleep(time_sleep)


def init(ip, puerto, code): #Funcion para comunicarse con el servidor
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creo un socket, la conexión.
        sock.connect((ip, puerto)) #Me conecto a la ip y el servidor del socket

        sock.send('{}'.format(code).encode('UTF-8')) #Envío la petición al servidor
        time.sleep(time_sleep)

        respuesta = sock.recv(packet_size).decode('UTF-8') #Espero por su respuesta 
        if respuesta == 'accepte': #Si me deja entrar, ejecuto la funcion proceso en ese socket
            proceso(code, sock)
        else:
            _print('Rechazado por el proveedor')

        sock.close()

    except KeyboardInterrupt:
        _print('Cerrando conexiones...')
        sock.send('exit'.encode('UTF-8'))
        sock.close()
        
```

Archivo proveedor:

```
import threading 
import time
from random import choice
import socketserver
from storage import codes, packet_size, store, time_sleep, time_smoke
from utils import _print

global smoke 
smoke = False
global smoke_code

class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass 

class MyTCPServerHandler(socketserver.BaseRequestHandler): #Clase que creo para poder modificar el servidor con protocolo TCP
    bufer = ''

    def proceso(self):
        while True:
            mensaje = self.request.recv(packet_size).decode('UTF-8') #Recibo el mensaje del fumador
            if mensaje == 'need': #El fumador necesita un recurso
                _print('{}: Necesito {}'.format(store.get(self.code)['name'], store.get(self.code)['required']))
                if self.smoke_released: #Pongo el smoke y el smoke released a False porque no está fumando
                    self.smoke_released = False
                    global smoke 
                    smoke = False

            elif mensaje == 'enable': #El fumador puede fumar
                _print('{}: Termino de fumar'.format(store.get(self.code)['name']))
                self.smoke_released = True #True porque está fumando

            elif mensaje == 'ack':
                time.sleep(time_smoke)
            
            elif mensaje == 'exit':
                break
            time.sleep(time_sleep)

    def handle(self):#Funcion para manejar el servidor
        self.code = self.request.recv(packet_size).decode('UTF-8')
        self.rejected = False
        self.smoke_released = False
        _print('Conectando fumador...') #Intentamos conectar con el fumador tras su mensaje.
        if store.get(self.code)['flag'] is False: #Se conecta si flag es False
            store.get(self.code)['request'] = self.request
            store.get(self.code)['flag'] = True
            _print('Fumador aceptado *{}*'.format(store.get(self.code)['name']))
            self.request.send('accepte'.encode('UTF-8'))
            self.proceso()
        else:
            self.rejected = True
            _print('Fumador rechazado *{}*'.format(store.get(self.code)['name']))
            self.request.send('rejected'.encode('UTF-8'))

    def finish(self): #Cuando terminan todos de fumar
        _print('Fumador desconectado *{}*'.format(store.get(self.code)['name']))
        if self.rejected == False:
            store.get(self.code)['flag'] = False
        global smoke_code
        if smoke_code == self.code:
            global smoke 
            smoke = False
        
    def handle_timeout(self):
        print('Tiempo de espera agotado')

def verificar_conexion(): #Verifica si los fumadores están conectados
    while True:
        fumadores_activos = True
        for i in codes:
            if store[i].get('flag') is False: #Si flag es False, entonces los fumadores no están conectados
                fumadores_activos = False
                break
        time.sleep(time_sleep)
        if fumadores_activos and smoke is False: #Salgo si smoke es false porque entonces han terminado de fumar
            break
        else:
            if fumadores_activos is False: #Si no han fumado pero no se han conectado
                _print('Esperando a todos los fumadores')


def init(puerto):
    try:
        servidor = MyTCPServer(('0.0.0.0', puerto), MyTCPServerHandler) #Creo el servidor llamando a la clase
        servidor.timeout = 10 
        servidor_hilo = threading.Thread(target = servidor.serve_forever) #Creo un hilo demonio para que se ejecute en la sombra
        servidor_hilo.timeout = 10
        _print('La tienda está abierta')
        servidor_hilo.daemon = True #Demonio para que escuche por peticiones en segundo plano
        servidor_hilo.start() #Inicializo el hilo

        while True:
            verificar_conexion() #Verifico si los fumadores están conectados
            global smoke_code
            smoke_code = choice(codes)
            _print('Tengo disponible {}'.format(store.get(smoke_code)['required'])) #Le doy el material que necesita el fumador
            global smoke
            smoke = True
            store.get(smoke_code)['request'].send('enable'.encode('UTF-8')) #Envío el mensaje de que ya tiene el recurso
            _print('Fumador {} servido'.format(store.get(smoke_code)['name']))

    except KeyboardInterrupt:
        _print('Cerrando conexiones...')
        servidor.shutdown()
        servidor.server_close()
                        
```

Archivo storage:

```
global store
codes = ('1', '2', '3', '4', '5')
store = {
    '1': {'name': 'Papel', 'required': 'Tabaco, Fósforos, Cenicero, Cerilla', 'flag': False, 'request': None},
    '2': {'name': 'Tabaco', 'required': 'Papel, Fósforos, Cenicero, Cerilla', 'flag': False, 'request': None},
    '3': {'name': 'Fósforos', 'required': 'Tabaco, Papel, Cenicero, Cerilla', 'flag': False, 'request': None},
    '4': {'name': 'Cenicero', 'required': 'Tabaco, Fósforos, Papel, Cerilla', 'flag': False, 'request': None},
    '5': {'name': 'Cerilla', 'required': 'Tabaco, Fósforos, Cenicero, Papel', 'flag': False, 'request': None},
}

time_smoke = 5
time_sleep = 1
packet_size = 1024
```

Archivo utils:

```
from datetime import datetime

def _print(mensaje):
    print('[{}] {}'.format(datetime.today(), mensaje))
```
Archivo main:

```
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
    os.system('cls')
    while True:
        print('1. Proveedor')
        print('2. Fumador (5 opciones)')
        type = input('Opcion: ')
        if type in ['1', '2']:
            break
        else:
            os.system('cls')
    os.system('cls')
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
                os.system('cls')
        ip = input('IP del proveedor: ')
        from fumador import init
        init(ip, get_puerto(), type)
```
