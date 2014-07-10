'''
Created on 10.07.2014

@author: markushinkelmann
'''
import SocketServer
from control.sockets.GameSocketHandler import GameSocketHandler
from control.sockets.websocketserver import WebSocketsHandler

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(("localhost", 9999), GameSocketHandler)
    server.serve_forever()
    
    
    #s1 = GameSocketHandler()