import socket
import time

from storage import packet_size, store, time_sleep, time_smoke
from utils import _print

def proceso(code, request):
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


