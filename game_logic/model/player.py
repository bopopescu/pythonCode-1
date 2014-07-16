# coding=utf-8
__author__ = 'M'

class Player:

    def __init__(self, name):
        self.__name = name

    def getMatchId(self):
        return self.__matchId
    def __str__(self):
        return 'Player session_id={:n}'.format(self.__sessionID)

    def getMatch(self):
        return self.__match

    def setMatchId(self, matchId):
        self.__matchId = matchId
        
    def getName (self):
        return self.__name