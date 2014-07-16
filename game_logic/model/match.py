# coding=utf-8
__author__ = 'M'

from game_logic.utils.classes import Point
import json

from ..utils.classes import Point
from ..calculation.calculation import Calculation
import time
import random

#import matplotlib.pyplot as plt

class Match:
    # dbID = 0
    # __players = []
    # __activePlayer = None
    # __horizon = []
    # __player_positions = []

    def __init__(self, players, world_width, horizon, player_x_positions):
        #TODO: DB-Werte holen / setzen ?

        self.__players = players
        self.__activePlayer = players[0] # erster Spieler beginnt
        self.__horizon = horizon
        self.__world_width = world_width
        self.__player_positions = dict()
        self.__matchId = "%f_%s" % (time.time(), random.randint(0,99999))

        # Spielerpositionen ermitteln und eintragen
        for i in xrange(len(players)):
            x = player_x_positions[i]
            print(x)
            self.__player_positions[players[i]] = Point(x, horizon[x])

        self.__calculation = Calculation(world_width, horizon, self.__player_positions)
    

    @property
    def calculation(self):
        return  self.__calculation

    def __str__(self):
        result = ''
        for player, pos in self.__player_positions.items():
            if len(result) > 0:
                result = result +'\n'
            result += player.__str__() + ': ' + pos.__str__()

        return result

    def calcHit(self, source, angle, speed):
        #TODO Rückgabe: Treffer, Treffer%, Flugbahn
        for player in self.__players:
            # TODO: für mehrere Ziele anpassen
            # berechnet z.Zt. nur für erstes Ziel
            if not player is source:
                return self.__calculation.calcHit(source, player, angle, speed)

    @property
    def players(self):
        return self.__players

    @property
    def activePlayer(self):
        return self.__activePlayer

    @activePlayer.setter
    def activePlayer(self, active_player):
        self.__activePlayer = active_player

    @property
    def horizon(self):
        return self.__horizon
    
    def getMatchId (self):
        return self.__matchId
    
    def getPlayerPostion (self, player):
        return self.__player_positions[player]