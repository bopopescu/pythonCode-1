__author__ = 'M'
from match import Match

class Player:
    dbID = 0
    sessionID = 0
    __match = None

    def __init__(self):
        #TODO Player / Match DB-Werte holen / setzen
        self.dbID = 0
        self.__match = None
        self.sessionID = 0

    def getMatch(self):
        return self.__match

    def setMatch(self, match):
        self.__match = match