'''
Created on 10.07.2014

@author: markushinkelmann
'''
import SocketServer
from control.sockets.GameSocketHandler import GameSocketHandler

'''Hauptschleife'''
if __name__ == '__main__':
    '''für lokales Lan :-) '''
	server = SocketServer.ThreadingTCPServer(("", 9999), GameSocketHandler)
    '''server = SocketServer.ThreadingTCPServer(("", 9999), GameSocketHandler)'''
    server.allow_reuse_address = True
    server.serve_forever()