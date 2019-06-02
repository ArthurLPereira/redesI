import socket
import sys
import time
import random
import json


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

class TCPServer():
    tcp = None
    HOST = ''
    PORT = 6969
    grid = [[]]
    ships = {}
    shots = []

    def __init__(self, host='', port=5000, random=False):
        if host is None or port is None:
            raise Exception('MISSING ARGUMENTS')
        
        self.random = random
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
        # Entrada padrão para teste
        entrada_x = [0, 6, 0, 2, 5, 9, 8, 0, 3, 3]
        entrada_y = [0, 0, 2, 4, 2, 4, 2, 6, 6, 9]
        entrada_c = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
        ite = -1
        for barco in lista_barcos:

            for i in range(barco['quantia']):
                navio = barco['nome']+str(i)
                print("\tposicionando {}".format(navio))
                size = barco['size']
                intercecao = True
                ite +=1
                while intercecao:
                    x = random.randrange(0,10) if self.random else entrada_x[ite]
                    y = random.randrange(0,10) if self.random else entrada_y[ite]
                    orientacao = bool(random.randint(0, 99)%2) if self.random else entrada_c[ite]
                    
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
                                                    'fim': (x+size-1, y),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                            else:
                                                distancia = 10 - size -1
                                                self.ships[navio] = {
                                                    'inicio': (distancia, y),
                                                    'fim': (distancia+size-1, y),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                        else:
                                            if y+size-1 < 10:
                                                self.ships[navio] = {
                                                    'inicio': (x, y),
                                                    'fim': (x, y+size-1),
                                                    'size': size,
                                                    'hits': []
                                                }
                                                posicionado = True
                                            else:
                                                distancia = 10 - size -1
                                                self.ships[navio] = {
                                                    'inicio': (x, distancia),
                                                    'fim': (x, distancia+size-1),
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
                    if self.random:
                        for key in self.ships.keys():
                            if key != navio:
                                if  (self.ships[key]['fim'][1] >= self.ships[navio]['inicio'][1] >= self.ships[key]['inicio'][1] or \
                                        self.ships[key]['fim'][1] >= self.ships[navio]['fim'][1] >= self.ships[key]['inicio'][1]) or \
                                            (self.ships[key]['fim'][0] >= self.ships[navio]['inicio'][0] >= self.ships[key]['inicio'][0] or \
                                                self.ships[key]['fim'][0] >= self.ships[navio]['fim'][0] >= self.ships[key]['inicio'][0]):
                                        intercecao = True
                self.posiciona_no_campo(navio, orientacao)
                # print('\t{} posicionado!'.format(navio))

    def posiciona_no_campo(self, navio, orientacao):
        if orientacao:

            for x in range(self.ships[navio]['inicio'][0], self.ships[navio]['fim'][0]+1):
                # print('O')
                self.grid[x][self.ships[navio]['inicio'][1]] = "O"
        else:
            for y in range(self.ships[navio]['inicio'][1], self.ships[navio]['fim'][1]+1):
                # print('O')
                self.grid[self.ships[navio]['inicio'][0]][y] = "O"
        pass

    def is_hit(self, x, y):
        for key in self.ships.keys():
            if self.ships[key]['fim'][1] >= y >= self.ships[key]['inicio'][1] and\
                self.ships[key]['fim'][0] >= x >= self.ships[key]['inicio'][0]:
                if str('{},{}'.format(x,y)) not in self.ships[key]['hits']:
                    self.ships[key]['hits'].append(str('{},{}'.format(x,y)))
                    print('{} was hit!'.format(key))
                    self.grid[x][y] = 'HIT'
                    if len(self.ships[key]['hits']) == self.ships[key]['size']:
                        print('Ship sunk....')
                        self.ships.pop(key)
                    return True
        self.grid[x][y] = 'X' if self.grid[x][y] != 'HIT' else self.grid[x][y]
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
        self.create_ships()
        print('ships created')
        for ship in self.ships.keys():
            print(ship, self.ships[ship])
        self.print_grid()
        while True:
            msg = con.recv(4096)
            if not msg:
                raise Exception('EMPTY MESSAGE')

            data = json.loads(msg.decode())
            print(data)
            hit = self.is_hit(data['x'], data['y'])
            x, y = self.shoot()
            print(len(self.ships))
            response = {
                'hit': hit,
                'x': x,
                'y': y,
                'gameover': len(self.ships) == 0
            }
            con.send((str.encode(json.dumps(response))))

            

            

    