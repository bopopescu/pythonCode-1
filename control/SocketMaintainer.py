'''
Created on 10.07.2014

@author: markushinkelmann
'''

class SocketMaintainer(object):
    '''
    Singleton Class, which will manage all open sockets
    '''
    _instance = None
    __connectedClients = {}
    
    
    def __new__(cls, *args, **kwargs):
        '''
        Function called, when a new class is initiated
        '''
        if not cls._instance:
            cls._instance = super(SocketMaintainer, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    
    def clientConnected (self, connectionID, handler):
        '''
        Function called when a new client is connected
        '''
        self.__connectedClients[connectionID] = handler
        
        
    def clientDisconnected (self, connectionID):
        '''
        Function Called when a client disconnected
        ''' 
        del (self.__connectedClients[connectionID])
        