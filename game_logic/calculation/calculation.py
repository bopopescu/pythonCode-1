__author__ = 'M'

import math
from player import Player
from match import Match

class Calculation:
    __horizon = []
    __height = 0
    __width = 0

    def __init__(self, height, width, horizon):
        self.__height = 0
        self.__width = 0
        self.__horizon = 0

    def calc(self, source, target, angle, power):
        """

        :param source: Player
        :param target: Player
        :param angle: Double
        :param power: Double
        :return: Double
        """
        #TODO: Treffer / Damage berechnen
        return 0

    def calcHorizonHeight(self, x):
        return -1

    def testHorizon(self):
        result = False

