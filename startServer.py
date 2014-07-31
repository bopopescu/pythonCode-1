'''
Created on 10.07.2014

@author: markushinkelmann
'''
import SocketServer
from control.sockets.GameSocketHandler import GameSocketHandler


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(("localhost", 9999), GameSocketHandler)
    server.serve_forever()