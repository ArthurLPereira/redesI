import socket
import sys
import time
import random
import json


SHIP_TYPES = ['porta-aviao', ]
class TCPServer():
    tcp = None
    HOST = ''
    PORT = 6969
    grid = [[]]
    ships = {}
    shots = []

    def __init__(self, host='', port=5000):
        if host is None or port is None:
            raise Exception('MISSING ARGUMENTS')
        
        self.grid = [[' ' for i in range(10)] for j in range(10)]
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = host if len(host) > 0 else socket.gethostbyname(socket.gethostname())
        self.PORT = port
        origin = (host, port)
        self.tcp.bind(origin)
        self.tcp.listen(1)
        self.ships = {}
        self.shots = []
        print('On HOST {} listening to PORT {}'.format(self.HOST, self.PORT))

    def start(self):
        self.create_ships()
        print('ships created')
        begining = time.time()
        print('Start at', begining)
        while True:
            elapsed = time.time() - begining
            con, client = self.tcp.accept()
            if elapsed > 300:
                con.close()
                raise TimeoutError(elapsed)
            
            try:
                self.game(con, client)
            except Exception as exp:
                print(exp)
            finally:
                con.close()

    def close(self):
        self.tcp.close()
        print('Connection on {}:{} closed'.format(self.HOST, self.PORT))

    def create_ships(self):
        print('Posicionando Frota')

        self.ships['porta-aviao'] = {
            'inicio': (random.randrange(0, 6), random.randrange(0, 10)),
            'hits': [],
            'size': 5
        }
        self.ships['porta-aviao'] = {
            'fim': (self.ships['porta-aviao']['inicio'][0]+4, self.ships['porta-aviao']['inicio'][1])
        }
            
        print('\tporta-aviao posicionado')

        for x in range(2):
            navio = 'navio-tanque{}'.format(x)
            maxini = 7
            size = 4
            intercecao = True
            while intercecao:
                self.ships[navio] = {
                    'inicio': (random.randrange(0, maxini), random.randrange(0, 10)),
                    'hits': [],
                    'size': size
                }
                
                self.ships[navio] = {
                    'fim': (self.ships[navio]['inicio'][0]+size-1, self.ships[navio]['inicio'][1])
                }
                intercecao = False
                for key in self.ships.keys():
                    if key != navio:
                        if intercecao and self.ships[key]['inicio'][1] == self.ships[navio]['inicio'][1] and \
                            (self.ships[key]['inicio'][0] >=self.ships[navio]['inicio'][0] >= self.ships[key]['inicio'][0] or \
                                self.ships[key]['inicio'][0] >=self.ships[navio]['fim'][0] >= self.ships[key]['inicio'][0]):
                                intercecao = True
                                break
            print('\t{} posicionado'.format(navio))

        for x in range(3):
            navio = 'contratorpedeiro{}'.format(x)
            maxini = 8
            size = 3
            intercecao = True
            while intercecao:
                self.ships[navio] = {
                    'inicio': (random.randrange(0, maxini), random.randrange(0, 10)),
                    'hits': [],
                    'size': size
                }
                
                self.ships[navio] = {
                    'fim': (self.ships[navio]['inicio'][0]+size-1, self.ships[navio]['inicio'][1])
                }

                intercecao = False
                for key in self.ships.keys():
                    if key != navio:
                        if intercecao and self.ships[key]['inicio'][1] == self.ships[navio]['inicio'][1] and \
                            (self.ships[key]['inicio'][0] >=self.ships[navio]['inicio'][0] >= self.ships[key]['inicio'][0] or \
                                self.ships[key]['inicio'][0] >=self.ships[navio]['fim'][0] >= self.ships[key]['inicio'][0]):
                                intercecao = True
                                break
            print('\t{} posicionado'.format(navio))

        for x in range(4):
            navio = 'submarino{}'.format(x)
            maxini = 9
            size = 2
            intercecao = True
            while intercecao:
                self.ships[navio] = {
                    'inicio': (random.randrange(0, maxini), random.randrange(0, 10)),
                    'hits': [],
                    'size': size
                }
                
                self.ships[navio] = {
                    'fim': (self.ships[navio]['inicio'][0]+size-1, self.ships[navio]['inicio'][1])
                }

                intercecao = False
                for key in self.ships.keys():
                    if key != navio:
                        if intercecao and self.ships[key]['inicio'][1] == self.ships[navio]['inicio'][1] and \
                            ((self.ships[key]['fim'][0] >= self.ships[navio]['inicio'][0] and self.ships[navio]['inicio'][0] >= self.ships[key]['inicio'][0]) or \
                                (self.ships[key]['fim'][0] >= self.ships[navio]['fim'][0] and self.ships[navio]['fim'][0] >= self.ships[key]['inicio'][0])):
                                intercecao = True
                                break
            print('\t{} posicionado'.format(navio))
        return    

    def is_hit(self, x, y):
        for key in self.ships.keys():
            if y == self.ships[key]['inicio'][0] and\
                (self.ships[key]['inicio'][0] >= x and\
                 x >= self.ships[key]['inicio'][0]):
                if x+','+y not in self.ships[key]['hits']:
                    self.ships[key]['hits'].append(x+','+y)
                    if len(self.ships[key]['hits']) == self.ships[key]['size']:
                        print('ship sunk')
                        self.ships.pop(key)
                    return True
        return False

    def shoot(self):
        while True:
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)
            translated = x+','+y
            if translated not in shots:
                self.shots.append(translated)
                return x, y

    def game(self, con, client):
        print('Playing with', client)
        while True:
            msg = con.recv(4096)
            if not msg:
                raise Exception('EMPTY MESSAGE')

            data = json.loads(msg)
            hit = self.is_hit(data['x'], data['y'])
            x, y = self.shoot()
            response = {
                'hit': hit,
                'x': x,
                'y': y
            }
            con.send(json.dumps(response))

            

            

    