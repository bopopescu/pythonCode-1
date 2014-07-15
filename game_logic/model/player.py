# coding=utf-8
__author__ = 'M'
import match

class Player:

    def __init__(self, db_id, session_id):
        #TODO Player / Match DB-Werte holen / setzen
        self.__dbID = db_id
        self.__sessionID = session_id

    def getMatch(self):
        return self.__match

    def setMatch(self, match):
        self.__match = match