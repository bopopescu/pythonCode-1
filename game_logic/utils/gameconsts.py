__author__ = 'M'

class Consts:
    PLAYER_RADIUS = 10
    BULLET_RADIUS = 3
    WORLD_WIDTH = 600
    g = 9.81
    
    
    
    
    
    #Constants for Client State handling
    CONNECTED = 0
    WAITFORPLAYER = 1
    GAMERUNNING = 2
    GAMEFINSIHED = 3
    
    #Constants for Server commands
    ##############################
    
    #incoming
    LOGON = "Logon"
    FIRE = "Fire"
    
    #outgoing
    WAITFORPLAYERMESSAGE = "WaitForPlayer"
    PLAYERAVAIBLE = "PlayerAvaible"
    GAMEDATA = "GameData"
    PLAYER1 = "Player1"
    PLAYER2 = "Player2"
    FIRED = "Fired"
    MAPHORIZON = "MapHorizon"