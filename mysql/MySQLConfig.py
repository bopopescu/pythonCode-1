'''
Created on 31.07.2014

@author: markushinkelmann
'''

class MySQLConfig(object):
    '''
    Class which provides the configuration to connect the mysql database
    '''
    HOST = 'localhost'
    DATABASE = 'tankcommander'
    USER = 'root'
    PASSWORD = ''
    PORT = 3306
    
    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True
    
    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
            }