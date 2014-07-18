# coding=utf-8
__author__ = 'M'

class Player:

    def __init__(self, name):
        self.__name = name

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