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