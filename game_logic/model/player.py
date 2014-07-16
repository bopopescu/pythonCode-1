# coding=utf-8
__author__ = 'M'
import match

class Player:

    def __init__(self, db_id, session_id):
        #TODO Player / Match DB-Werte holen / setzen
        self.__dbID = db_id
        self.__sessionID = session_id

    def __str__(self):
        return 'Player session_id={:n}'.format(self.__sessionID)

    def getMatch(self):
        return self.__match

    def setMatch(self, match):
        self.__match = match