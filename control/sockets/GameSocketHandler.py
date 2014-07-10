'''
Created on 10.07.2014

@author: markushinkelmann
'''
from control.sockets.websocketserver import WebSocketsHandler
from control.SocketMaintainer import SocketMaintainer
import random
import time

class GameSocketHandler(WebSocketsHandler):
    '''
    Socket Handler for the game commnication
    '''
    __socketID = None
    
    def __init__(self, request, client_address, server):
        '''
        Constructor
        '''
        #Get an instance from the socket maintainer class
        self.__socketMaintainer = SocketMaintainer()
        self.__socketID = "%f_%s" % (time.time(), random.randint(0,99999))
        
        WebSocketsHandler.__init__(self, request, client_address, server)
    
   
    def setup(self):
        '''
        Overwritten function called when the socket connection is created
        '''
        WebSocketsHandler.setup(self)
        self.__socketMaintainer.clientConnected(self.__socketID, self)
    
    def handle(self):
        '''
        Overwritten function called, when a data is to handle
        '''
        try:
            WebSocketsHandler.handle(self)
        except Exception, ex:
            print "Error during handling a request %s" % str(ex)
    

    def handleError (self):
        '''
        Function called, when an error occurs 
        '''
        print "Connection lost from client %s" % self.client_address
        self.__socketMaintainer.clientDisconnected(self.__socketID)
        
    
    
    
    