# coding=utf-8
__author__ = 'M'

class Player:

    def __init__(self, name, socket):
        self.__name = name
        self.__socket = socket
        self.damage = 0
        self.__match = None


    def getMatch (self):
        return self.__match
    
    def setMatch (self, match):
        self.__match = match
        
    def __str__(self):
        return 'Player ' + self.__name

    @property
    def name (self):
        return self.__name

    def add_damage(self, damage):
        """
        Fügt die Beschädigung hinzu
        :param damage: neue Beschädigung
        :return: Gesamtbeschädigung
        """
        self.__damage += damage
        if self.__damage > 1:
            self.__damage = 1

    
    @property
    def socket (self):
        return self.__socket
    
    
    def getJSON (self):
        '''
        Function which will create a JSON Object for the Player
        '''
        
        template = """
        {
            "Name":     "%(__name__)s",
            "ID":       "%(__id__)s",
            "Position": %(__position__)s
            "Damage":   %(__damage__)f
        }
                   """
    
        if self.__match == None:
            position = "\"\""
        else:
            position = str(self.__match.getPlayerPostion(self))
        
        subst = {
                 "__name__"     : self.__name,
                 "__id__"       : self.__socket.getSocketId(),
                 "__position__" : position,
                 "__damage__"   : self.damage
                 }
        
        
        return template % subst