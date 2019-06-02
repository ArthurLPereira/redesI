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
        self.print_grid()
        begining = time.time()
        print('Start at', begining)
        while True:
            elapsed = time.time() - begining
            con, client = self.tcp.accept()
            if elapsed > 1800:
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

    def print_grid(self):
        print('y/x', '\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t'.format(*range(10)))
        for y in range(10):
            print(y, '|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|'.format(*[self.grid[x][y] for x in range(10)]))
    
    def create_ships(self):
        print('Posicionando Frota')
        lista_barcos = [{'nome': 'porta-aviao', 'size': 5, 'quantia': 1}, {'nome': 'navio-tanque', 'size': 4, 'quantia': 2},
            {'nome': 'contratorpedeiro', 'size': 3, 'quantia': 3}, {'nome': 'submarino', 'size': 2, 'quantia': 4}]
        
        for barco in lista_barcos:
            for i in range(barco['quantia']):
                navio = barco['nome']+str(i)
                print("\tposicionando {}".format(navio))
                size = barco['size']
                intercecao = True
                while intercecao:
                    x = random.randrange(0,10)
                    y = random.randrange(0,10)
                    orientacao = bool(random.randint(0, int(time.time()))%2)
                    posicionado = False
                    while not posicionado:
                        if x>= 0:
                            if x < 10:
                                if y >= 0:
                                    if y < 10:
                                        if orientacao:
                                            if x+size-1 < 10:
                                                self.ships[navio] = {
                                                    'inicio': (x, y),
                                                    'fim': (x+size, y),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                            else:
                                                distancia = 10 - size -1
                                                self.ships[navio] = {
                                                    'inicio': (distancia, y),
                                                    'fim': (distancia+size, y),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                        else:
                                            if y+size-1 < 10:
                                                self.ships[navio] = {
                                                    'inicio': (x, y),
                                                    'fim': (x, y+size),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                            else:
                                                distancia = 10 - size -1
                                                self.ships[navio] = {
                                                    'inicio': (x, distancia),
                                                    'fim': (x, distancia+size),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                    else:
                                        y = 9
                                else:
                                    y = 0
                            else:
                                x = 9
                        else:
                            x = 0
                    intercecao = False
                    for key in self.ships.keys():
                        if key != navio:
                            if intercecao and \
                                (self.ships[key]['inicio'][1] >=self.ships[navio]['inicio'][1] >= self.ships[key]['inicio'][1] or \
                                    self.ships[key]['inicio'][1] >=self.ships[navio]['fim'][1] >= self.ships[key]['inicio'][1]) and \
                                        (self.ships[key]['inicio'][0] >=self.ships[navio]['inicio'][0] >= self.ships[key]['inicio'][0] or \
                                            self.ships[key]['inicio'][0] >=self.ships[navio]['fim'][0] >= self.ships[key]['inicio'][0]):
                                    intercecao = True
                                    print('Interceção de Navios')
                                    break
                    self.posiciona_no_campo(navio, orientacao)
                    print('\t{} posicionado!'.format(navio))

    def posiciona_no_campo(self, navio, orientacao):
        if orientacao:
            for x in range(self.ships[navio]['inicio'][0],self.ships[navio]['fim'][0]):
                self.grid[x][self.ships[navio]['inicio'][1]] = "O"
        else:
            for y in range(self.ships[navio]['inicio'][1], self.ships[navio]['fim'][1]):
                self.grid[self.ships[navio]['inicio'][0]][y] = "O"
        pass

    def is_hit(self, x, y):
        
        for key in self.ships.keys():
            print('is {} hit?'.format(key))
            if y == self.ships[key]['inicio'][1] and\
                (self.ships[key]['fim'][0] >= x and\
                 x >= self.ships[key]['inicio'][0]):
                if '{},{}'.format(x,y) not in self.ships[key]['hits']:
                    print('HIT!')
                    self.ships[key]['hits'].append('{},{}'.format(x,y))
                    if len(self.ships[key]['hits']) == self.ships[key]['size']:
                        print('ship sunk')
                        self.ships.pop(key)
                    return True
        return False

    def shoot(self):
        while True:
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)
            translated = '{},{}'.format(x,y)
            if translated not in self.shots:
                self.shots.append(translated)
                return x, y

    def game(self, con, client):
        print('Playing with', client)
        while True:
            msg = con.recv(4096)
            if not msg:
                raise Exception('EMPTY MESSAGE')

            data = json.loads(msg.decode())
            print(data)
            hit = self.is_hit(data['x'], data['y'])
            x, y = self.shoot()
            response = {
                'hit': hit,
                'x': x,
                'y': y,
                'gameover': len(self.ships) == 0
            }
            con.send((str.encode(json.dumps(response))))

            

            

    