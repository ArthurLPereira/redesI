from Cliente import TCPClient
import sys

if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = sys.argv[2]
        client = TCPClient(port=int(port))
        client.start()
    except Exception as exp:
        print(exp)