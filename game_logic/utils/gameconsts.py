# coding=utf-8
__author__ = 'M'

class Consts:
    PLAYER_RADIUS = 10
    BULLET_RADIUS = 3
    WORLD_WIDTH = 600

    MIN_HORIZON_HEIGHT = 0
    MAX_HORIZON_HEIGHT = 400
    MIN_SAMPLING_POINTS = 10 # minimale Anzahl Stuetzstellen f. Horizont
    MAX_SAMPLING_POINTS = 20 # maximale Anzahl Stuetzstellen f. Horizont
    GAP_TO_FIRST_SAMPLING_POINT = 50 # Abstand bis zur ersten / letzten Stuetzstelle

    TIME_RESOLUTION = 0.0009
    # 0.001  reicht fuer 99,47% Treffer bei senkrechtem Schuss
    # 0.0009 reicht fuer 99,63% Treffer bei senkrechtem Schuss

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
    WRONGTURN = "WrongTurn"