import socket
import sys
import time
import random
import json

class TCPClient():
    def __init__(self, host='', port=5000):
        if port is None:
            raise Exception('MISSING ARGUMENTS')
        
        self.ships = []
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

    def read_coords(self):
        while True:
            x = input()
            if x > 0 and x < 9:
                return x

    def is_hit(self, x, y):
        for key in self.ships.keys():
            if self.ships[key]['fim'][1] >= y >= self.ships[key]['fim'][1] and\
                self.ships[key]['inicio'][0] >= x >= self.ships[key]['fim'][0]:
                if str(x+','+y) not in self.ships[key]['hits']:
                    self.ships[key]['hits'].append(str(x+','+y))
                    grid[x][y] = 'HIT'
                    if len(self.ships[key]['hits']) == self.ships[key]['size']:
                        print('ship sunk')
                        self.ships.pop(key)
                    return True
        self.grid[x][y] = 'X'
        return False

    def play(self):

        print ('Para sair use CTRL+X\n')
        print('Posicione sua Frota!')
        self.read_boats()
        print("Pressione enter para continuar!")
        msg = input()
        while msg != '\x18':
            
            while msg != 'A':
                # print(matriz)
                msg = input()
            
            request = {
                'x': read_coords(),
                'y': read_coords()
            }
            tcp.send(json.dumps(request))
            
            data = tcp.recv(4096)
            data = json.loads(data)
            if data.get('hit', False):
                self.server_grid[request['x']][request['y']] =  'HIT'
            else: 
                self.server_grid[request['x']][request['y']] =  'X'

            msg = input()
                
        tcp.close()


    def read_boats(self):
        lista_barcos = [{'nome': 'porta-aviao', 'size': 5, 'quantia': 1}, {'nome': 'navio-tanque', 'size': 4, 'quantia': 2},
          {'nome': 'contratorpedeiro', 'size': 3, 'quantia': 3}, {'nome': 'submarino', 'size': 2, 'quantia': 4}]
        
        for barco in lista_barcos:
            for i in range(barco['quantia']):
                navio = barco['nome'] + i
                size = barco['size']
                intercecao = True
                while intercecao:
                    x = input('x:')
                    y = input('y:')
                    vertical = input('Orientacao(1 para horizontal e 0 para vertical):')
                    posicionado = False
                    while not posicionado:
                        if x>= 0:
                            if x < 10:
                                if y >= 0:
                                    if y < 10:
                                        if vertical:
                                            if x+size < 10:
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
                                            if y+size < 10:
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
                    self.posiciona_no_campo(navio)
    
    def posiciona_no_campo(self, navio):
        pass

if __name__ == "__main__":
    HOST = input("Insira o endereco IP: ")            # Endereco IP do Servidor
    PORT = input("Insira a porta de comunicacao: ")   # Porta que o Servidor esta

    pass