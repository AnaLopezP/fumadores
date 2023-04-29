import socket
import time

from storage import packet_size, store, time_sleep, time_smoke
from utils import _print

def proceso(code, request):
    mensaje = ""
    while True:
        if mensaje != 'ack':
            _print("Esperando {}!".format(store.get(code)['required']))
            request.send('need'.encode('UTF-8'))
        
        mensaje = request.recv(packet_size).decode('UTF-8')
        if mensaje == 'enable':
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