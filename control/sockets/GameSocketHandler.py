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
import json

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
        self.__keepAlive = True
        
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
            while self.__keepAlive:
                if not self.handshake_done:
                    self.handshake()
                else:
                    self.read_next_message()
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
        self.__socketMaintainer.clientDisconnected(self.__socketID)
        self.close()
        raise  ex # TODO: Just for debug
        
        
    def on_message(self, message):
        '''
        Function called when a new message received
        '''
        #Handle the message
        keyword, paramString = message.split(":", 1)
        resultDict = json.loads(paramString)
                
        #handle the keywords
        if keyword == Consts.LOGON:
            self.__state = Consts.WAITFORPLAYER
            self.__playerObject = Player(resultDict[Consts.PLAYERNAME], self)
            self.__socketMaintainer.playerWantToPlay(self.__socketID)
        elif keyword == Consts.FIRE:
            self.__receivedFireCommand(resultDict[Consts.ANGLE], resultDict[Consts.POWER])
        else:
            self.close()
            
    
    def matchStarted (self, match):
        '''
        Function called, when a Match is started
        '''
        self.__match = match
        self.__state = Consts.GAMERUNNING
        self.__playerObject.setMatch(match)
        
        self.send_message("%s" % (Consts.PLAYERAVAILABLE))
    
    def __receivedFireCommand (self, angle, power):
        '''
        Function called when the player received a fire command
        '''
        #Check if it allowed for the player to fire
        if self.__match.activePlayer != self.__playerObject:
            self.send_message(Consts.WRONGTURN)
            return
        
        #Make the match calculation
        flightPath = self.__match.calc_flugbahn(self.__playerObject, float(angle), float(power))
        
        message = self.__createJSON(flightPath)
        
        
        #Send the result to the clients
        messageString = "%s:%s" % (Consts.FIRED, message)
        
        for player in self.__match.players:
            player.socket.send_message(messageString)
         
        #Change the player in the match
        self.__match.activePlayer = self.__foundNextPlayer(self.__playerObject)
         
    
    def __createJSON (self, flightPath):
        '''
        Function which will create a JSON Object for the flight path
        '''
        #Define format values
        message = """
                  {
                      "StartPoint": %(__startPoint__)s,
                      "MaxYPoint":  %(__maxYPoint__)s,
                      "TimePoints": [%(__timePoints__)s],
                      "Hits":       [%(__hits__)s]
                  }
                  """
        
        hitObject = """
                    {
                        "X": "%(__X__)i",
                        "Y": "%(__Y__)i",
                        "T": "%(__T__).4f",
                        "Percent": "%(__percent__).4f",
                        "Player": "%(__player__)s" #TODO: Send the player object instead of an id
                    }
                    """
        
        hitObjects = []
        
        #Create the hit Objects
        for hit in flightPath.hits:
            if hit.target is None:
                target = "\"\""
            else:
                target = target.getJSON()
            
            subst = {
                     "__X__" : hit.x,
                     "__Y__" : hit.y,
                     "__T__" : hit.t,
                     "__percent__" : hit.percent,
                     "__player__" : target
                     }
            
            hitObjects.append(hitObject % subst)
        
        
        #Create the json Template
        subst = {
                     "__startPoint__" : str(flightPath.start_point),
                     "__maxYPoint__" : str(flightPath.max_y_point),
                     "__timePoints__" : ",".join(str(x) for x in flightPath.time_points),
                     "__hits__" : ",".join(hitObjects)
                }
        
        return message % subst
    
    def __foundNextPlayer (self, currentPlayer):
        '''
        Function which will found the player for the next turn
        '''
        
        i=0
        for player in self.__match.players:
            i = i + 1
            if player == currentPlayer:
                break
                
                
        if i >= len(self.__match.players):
            i=0
            
        return self.__match.players[i] 

    
    def close (self):
        '''
        Function which will close the connection
        '''
        print "Close connection"
        self.__keepAlive=False
        self.request.close()
        
        

    #Getter + Setter Methods
    def getPlayerObject (self):
        return self.__playerObject
    
    def getSocketState (self):
        return self.__state
    
    def getSocketId (self):
        return self.__socketID
            
        
        