'''
Created on 10.07.2014

@author: markushinkelmann
'''
from control.sockets.websocketserver import WebSocketsHandler
from control.SocketMaintainer import SocketMaintainer
from game_logic.utils.gameconsts import Consts
from game_logic.model.player import Player
import random
import time

class GameSocketHandler(WebSocketsHandler):
    '''
    Socket Handler for the game commnication
    '''
    
    def __init__(self, request, client_address, server):
        '''
        Constructor
        '''
        #Get an instance from the socket maintainer class
        self.__socketMaintainer = SocketMaintainer()
        self.__socketID = "%f_%s" % (time.time(), random.randint(0,99999))
        self.__state = Consts.CONNECTED
        self.__match = None
        
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
            self.__handleError(ex)
    
    def send_message(self, message):
        try:
            WebSocketsHandler.send_message(self, message)
        except Exception, ex:
            self.__handleError(ex)
    
    def __handleError (self, ex):
        '''
        Function called, when an error occurs 
        '''
        print "Connection lost from client %s with error: %s" % (self.client_address, str(ex))
        raise  ex
        self.__socketMaintainer.clientDisconnected(self.__socketID)
        
        
    def on_message(self, message):
        '''
        Function called when a new message received
        '''
        #Handle the message
        keyword, paramString = message.split("(")
        paramString = paramString[:-1]
        #Split the param String in a param array
        params = paramString.split(",")
        
        #handle the keywords
        if keyword == Consts.LOGON:
            self.__state = Consts.WAITFORPLAYER
            self.__playerObject = Player(params[0])
            self.__socketMaintainer.playerWantToPlay(self.__socketID)
            
    
    def matchStarted (self, match, oponentName):
        '''
        Function called, when a Match is started
        '''
        self.__match = match
        self.__state = Consts.GAMERUNNING
        
        self.send_message("%s(%s)" % (Consts.PLAYERAVAIBLE, oponentName))
        
    
    #Getter + Setter Methods
    def getPlayerObject (self):
        return self.__playerObject
    
    def getSocketState (self):
        return self.__state
    
    def getSocketId (self):
        return self.__socketID
            
        
        