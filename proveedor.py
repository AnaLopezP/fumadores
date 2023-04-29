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
                        