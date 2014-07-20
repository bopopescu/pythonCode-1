# coding=utf-8
from mysql.connector.constants import flag_is_set

__author__ = 'M'

import math

from game_logic.match_builder import MatchBuilder
from game_logic.model.player import Player
from game_logic.model.match import Match

if __name__ == '__main__':
    player1 = Player('A')
    player2 = Player('B')

    print(player1)
    print(player2)
    testMatch = MatchBuilder.get_match([player1, player2])
    print(testMatch)
    for i in xrange(10):
        angle = math.pi / 2
        speed = 200
        flugbahn = testMatch.calc_flugbahn(player1, angle, speed)
        print('Schusshöhe: {:.2f}'.format(flugbahn.max_y_point.y))
        for hit in flugbahn.hits:
            print('Treffer: ' + hit.__str__())
        print('')