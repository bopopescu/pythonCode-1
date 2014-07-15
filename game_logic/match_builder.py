# coding=utf-8
from _ast import Dict

__author__ = 'M'

from model.match import Match
import random
import math
from random import shuffle

class MatchBuilder:

    @staticmethod
    def __get_new_horizon(world_width):
        #TODO Random init mit x Stützpunkten

        result = [1]
        for i in xrange(1,100):
            result.append(result[i - 1] + 1)
        for i in xrange(100,500):
            result.append(100)
        for i in xrange(500,world_width):
            result.append(result[i - 1] - 1)

        return result

    @staticmethod
    def __get_new_player_x_positions(players, world_width):
        result = []

        # prüfen, ob Initialisierung / globales Objekt erforderlich ist
        random.seed()
        # etwas übertrieben kompliziert, evtl. können mehr als 2 Player spielen?
        parts_width = float(world_width) / (len(players) + 1)
        for i in xrange(len(players)):
            if (i <= len(players) / 2):
                result.append(int(round(i * parts_width + (parts_width * random.random()))))
            else:
                result.append(int(round((i + 1) * parts_width + (parts_width * random.random()))))

        return result

    @staticmethod
    def get_match(players, world_width):
        """
        Erstellt ein neues Match
        :rtype : Match
        """
        return Match(players, world_width, MatchBuilder.__get_new_horizon(world_width), MatchBuilder.__get_new_player_x_positions(players, world_width))