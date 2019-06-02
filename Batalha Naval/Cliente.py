import socket
import sys
import time
import random
import json

class TCPClient():
    def __init__(self, host='', port=5000):
        if port is None:
            raise Exception('MISSING ARGUMENTS')
        
        self.ships = {}
        self.grid = [[' ' for i in range(10)] for j in range(10)]
        self.server_grid = [[' ' for i in range(10)] for j in range(10)]
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = host if len(host) > 0 else socket.gethostbyname(socket.gethostname())
        self.PORT = port
    
    def start(self):
        dest = (self.HOST, self.PORT)
        self.tcp.connect(dest)
        print('Connected to {}:{}'.format(self.HOST, self.PORT))
        self.play()

    def read_coords(self, axis):
        while True:
            x = int(input('{}:'.format(axis)))
            if x >= 0 and x < 10:
                return x

    def is_hit(self, x, y):
        for key in self.ships.keys():
            if self.ships[key]['fim'][1] >= y >= self.ships[key]['inicio'][1] and\
                self.ships[key]['fim'][0] >= x >= self.ships[key]['inicio'][0]:
                if str('{},{}'.format(x,y)) not in self.ships[key]['hits']:
                    self.ships[key]['hits'].append(str('{},{}'.format(x,y)))
                    print('Oh no, {} got hit!'.format(key))
                    self.grid[x][y] = 'HIT'
                    if len(self.ships[key]['hits']) == self.ships[key]['size']:
                        print('MAYDAY MAYDAY! Ship sunk....')
                        self.ships.pop(key)
                    return True
        self.grid[x][y] = 'X' if self.grid[x][y] != 'HIT' else self.grid[x][y]
        return False

    def print_grids(self):
        print('Campo Adversário')
        print('y/x', '\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t'.format(*range(10)))
        for y in range(10):
            print(y, '|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|'.format(*[self.server_grid[x][y] for x in range(10)]))
        print("\nSeu Campo")
        print('y/x', '\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t'.format(*range(10)))
        for y in range(10):
            print(y, '|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}\t|'.format(*[self.grid[x][y] for x in range(10)]))

    def play(self):

        print ('Para sair use CTRL+X\n')
        print('Posicione sua Frota!')
        self.read_boats()
        print("Pressione enter para continuar!")
        msg = input().upper()
        while msg != '\x18':
            
            while msg != 'A' and msg != '\x18':
                self.print_grids()
                msg = input().upper()
            
            if msg == '\x18': break
            
            request = {
                'x': self.read_coords('x'),
                'y': self.read_coords('y')
            }
            self.tcp.send(str.encode(json.dumps(request)))
            print('sent')
            data = self.tcp.recv(4096)
            data = json.loads(data.decode())
            print(data)
            if data.get('hit', False):
                print('YASSSS!')
                self.server_grid[request['x']][request['y']] =  'HIT'
            else: 
                print('DANG!')
                self.server_grid[request['x']][request['y']] =  'X' if self.server_grid[request['x']][request['y']] != 'HIT' else self.server_grid[request['x']][request['y']]
            
            if data['gameover']: 
                print('GAMEOVER, YOU WON!')
                break
            self.is_hit(data['x'], data['y'])

            if len(self.ships) == 0:
                print('ABANDON SHIP, WE\'RE GOING DOWN!!!')
                print('GAMEOVER, YOU LOST!')
                break
            msg = input().upper()             
        self.tcp.close()


    def read_boats(self):
        lista_barcos = [{'nome': 'porta-aviao', 'size': 5, 'quantia': 1}, {'nome': 'navio-tanque', 'size': 4, 'quantia': 2},
          {'nome': 'contratorpedeiro', 'size': 3, 'quantia': 3}, {'nome': 'submarino', 'size': 2, 'quantia': 4}]
        
        for barco in lista_barcos:
            for i in range(barco['quantia']):
                navio = barco['nome']+str(i)
                print("\tposicionando {}".format(navio))
                size = barco['size']
                intercecao = True
                while intercecao:
                    x = int(input('\t x:'))
                    y = int(input('\t y:'))
                    orientacao = bool(int(input('\t Orientacao(1 para horizontal e 0 para viertical):')))
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
                    self.posiciona_no_campo(navio, size,orientacao)
                    print('\t{} posicionado!'.format(navio))
    
    def posiciona_no_campo(self, navio, size, orientacao):
        if orientacao:
            for x in range(self.ships[navio]['inicio'][0],self.ships[navio]['fim'][0]):
                self.grid[x][self.ships[navio]['inicio'][1]] = "O"
        else:
            for y in range(self.ships[navio]['inicio'][1], self.ships[navio]['fim'][1]):
                self.grid[self.ships[navio]['inicio'][0]][y] = "O"
        pass