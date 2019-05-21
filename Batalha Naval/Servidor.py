import socket
import sys
import time
import random


SHIP_TYPES = ['porta-aviões', ]
class TCPServer():
    tcp = None
    HOST = ''
    PORT = 6969
    grid = [[]]
    ships = {}

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
        print('On HOST {} listening to PORT {}'.format(self.HOST, self.PORT))

    def start(self):
        self.create_ships()
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
        
        self.ships['porta-aviões'] = {
            'inicio': (random.randrange(0, 5), random.randrange(0, 10))
        }
        
        self.ships['porta-aviões'] = {
            'fim': (self.ships['porta-aviões'][0]+5, self.ships['porta-aviões'][1])
        }

        return


    def game(self, con, client):
        print('Playing with', client)
        while True:
            msg = con.recv(4096)

            if not msg:
                raise Exception('EMPTY MESSAGE')
            
            print('hey')
    