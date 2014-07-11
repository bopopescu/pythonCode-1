__author__ = 'M'
from player import Player
import matplotlib.pyplot as plt

class Match:
    dbID = 0
    __players = []
    __activePlayer = None
    __horizon = []

    def __init__(self, players):
        """

        :param players: Player[]
        """
        #TODO: DB-Werte holen / setzen
        self.players = players
        self.__activePlayer = players[0]

    def getPlayers(self):
        return self.__players

    def getActivePlayer(self):
        return self.__activePlayer

    def setActivePlayer(self, active_player):
        """

        :type active_player: Player
        """
        self.__activePlayer = active_player

    def getHorizon(self):
        return self.__horizon