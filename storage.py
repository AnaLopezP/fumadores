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