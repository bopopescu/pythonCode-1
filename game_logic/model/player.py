# coding=utf-8
__author__ = 'M'

class Player:

    def __init__(self, name):
        self.__name = name

    def getMatchId(self):
        return self.__matchId

    def setMatchId(self, matchId):
        self.__matchId = matchId
        
    def getName (self):
        return self.__name