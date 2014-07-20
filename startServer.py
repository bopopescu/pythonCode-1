'''
Created on 10.07.2014

@author: markushinkelmann
'''
import SocketServer
from control.sockets.GameSocketHandler import GameSocketHandler
from control.sockets.websocketserver import WebSocketsHandler
from game_logic.model.player import Player
from game_logic import match_builder
from game_logic.utils.gameconsts import Consts


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(("localhost", 9999), GameSocketHandler)
    server.serve_forever()
    
    
    #s1 = GameSocketHandler()
    
    player1 = Player("A")
    player2 = Player("B")
    
    match = match_builder.MatchBuilder.get_match([player1, player2])
    
    
    
    coordinates = ",".join(str(value) for value in match.horizon)
    print "%s(%s:[%s])" % (Consts.GAMEDATA, Consts.MAPHORIZON, coordinates)
    