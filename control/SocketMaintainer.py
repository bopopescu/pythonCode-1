'''
Created on 10.07.2014

@author: markushinkelmann
'''

from game_logic.utils.gameconsts import Consts
from game_logic.match_builder import MatchBuilder
import json

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
        
    
    def playerWantToPlay (self, socketId):
        '''
        Function called, when a player want to play
        '''
        #Check if already a waiting player exists 
        waitingPlayer = self.__searchForConnections(Consts.WAITFORPLAYER, socketId)
        #Send the own player object to the client
        self.__connectedClients[socketId].send_message("%s:%s" % (Consts.PLAYER, self.__connectedClients[socketId].getPlayerObject().getJSON()))
        #Check if it possible to start a game
        if waitingPlayer is None:
            self.__connectedClients[socketId].send_message(Consts.WAITFORPLAYERMESSAGE)
        else:
            self.__startGame(waitingPlayer, socketId)
        
        
    def __searchForConnections (self, state, excluded):
        '''
        Search for a Connection with a specific state
        @param state: The state variable
        '''
        for connectionId in self.__connectedClients:
            if self.__connectedClients[connectionId].getSocketState() == state and self.__connectedClients[connectionId].getSocketId() != excluded:
                # Sort the client after waiting time
                return connectionId
            
        return None
    
    
    def __startGame (self, player1SocketId, player2SocketId):
        '''
        Function which will start a game
        '''
        #Create the match
        playerSockets = [self.__connectedClients[player1SocketId], self.__connectedClients[player2SocketId]]
        
        player1 = playerSockets[0].getPlayerObject()
        player2 = playerSockets[1].getPlayerObject()
        match = MatchBuilder.get_match([player1, player2]) # TODO: Handle with static constants
        
        #Inform the clients about the starting match
        playerSockets[0].matchStarted(match)
        playerSockets[1].matchStarted(match)
        
        #Send the game data
        for socket in playerSockets:
            coordinates = ",".join(str(value) for value in match.horizonSkeletonPoints)
            
            socket.send_message("%s: %s" % (Consts.PLAYER1, player1.getJSON()))
            socket.send_message("%s: %s" % (Consts.PLAYER2, player2.getJSON()))
            socket.send_message("%s: %s" % (Consts.PLAYERBEGINS, match.activePlayer.getJSON()))
            socket.send_message("%s:[%s]" % (Consts.MAPHORIZON, coordinates))