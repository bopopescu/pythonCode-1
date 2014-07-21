# coding=utf-8

__author__ = 'M'

import math

from game_logic.match_builder import MatchBuilder
from game_logic.model.player import Player

if __name__ == '__main__':
    player1 = Player('A',None)
    player2 = Player('B',None)

    testMatch = MatchBuilder.get_match([player1, player2])
    print(testMatch)
    for i in xrange(10):
        angle = math.pi / 4
        speed = 20
        flugbahn = testMatch.calc_flugbahn(player1, angle, speed)
        print('Schusshöhe: {:.2f}'.format(flugbahn.max_y_point.y))
        for hit in flugbahn.hits:
            print('Treffer: ' + hit.__str__())
        print('')