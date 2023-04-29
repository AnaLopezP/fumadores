import os

from storage import codes, store

def get_puerto():
    while True:
        try:
            puerto = int(input('Puerto (1024 - 49151): '))
            if puerto >= 1024 and puerto <= 49151:
                break
        except Exception:
            pass
    return puerto