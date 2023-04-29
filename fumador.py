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