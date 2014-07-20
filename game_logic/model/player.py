# coding=utf-8
__author__ = 'M'

class Player:

    def __init__(self, name, socket):
        self.__name = name
        self.__socket = socket
        self.damage = 0

    @property
    def match(self):
        return self.__match
    
    @match.setter
    def match(self, match):
        self.__match = match
        
    def __str__(self):
        return 'Player ' + self.__name

    @property
    def name (self):
        return self.__name

    def add_damage(self, damage):
        """
        F�gt die Besch�digung hinzu
        :param damage: neue Besch�digung
        :return: Gesamtbesch�digung
        """
        self.__damage += damage
        if self.__damage > 1:
            self.__damage = 1

    
    @property
    def socket (self):
        return self.__socket