# coding=utf-8
__author__ = 'M'

from ..utils.gameconsts import Consts
from ..utils.classes import Point
from ..calculation.calculation import Calculation
import time
import random

class Match:

    def __init__(self, players, world_width, horizon, player_x_positions):

        self.__players = players
        self.__activePlayer = players[0] # erster Spieler beginnt
        self.__horizon = horizon
        self.__world_width = world_width
        self.__player_positions = dict() # Position = Mittelpunkt des Players
        self.__id = "%f_%s" % (time.time(), random.randint(0,99999))

        # Spielerpositionen ermitteln und eintragen
        for i in xrange(len(players)):
            x = player_x_positions[i]
            # x = player_x_positions[0] # Test
            self.__player_positions[players[i]] = Point(x, horizon[x] + Consts.PLAYER_RADIUS)

        self.__calculation = Calculation(world_width, horizon, players, self.__player_positions)
    

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

    def calc_flugbahn(self, source, angle, speed):
        #TODO Rückgabe: Treffer, Treffer%, Flugbahn
        """
        Berechnet den Auftreffpunkt
        entweder Horizont (0% Damage)
        oder Player
        :param source: Player
        :param angle: Double (Radiant)
        :param speed: Double (m/s)
        :return: Hit
        """
        return self.__calculation.calc_flugbahn(source, angle, speed)

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
    
    @property
    def id (self):
        return self.__id
    
    def getPlayerPostion (self, player):
        return self.__player_positions[player]