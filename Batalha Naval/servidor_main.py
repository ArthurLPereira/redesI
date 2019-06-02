from Servidor import TCPServer
import sys

if __name__ == "__main__":
    try:
        port = sys.argv[1]
        server = TCPServer(port=int(port))

        server.start()
    except Exception as exp:
        print(exp)
