__author__ = 'M'
# coding=utf-8

import math

from game_logic.match_builder import MatchBuilder
from game_logic.model.player import Player
from game_logic.model.match import Match

if __name__ == '__main__':
    player1 = Player('A')
    player2 = Player('B')

    for i in xrange(1000):
        testMatch = MatchBuilder.get_match([player1, player2])
        angle = math.pi / 2
        speed = 60
        hit = testMatch.calcHit(player1, angle, speed)
        print(player1)
        print(player2)
        print(testMatch)
        print('Schusshöhe: ' +testMatch.calculation.calcHorizonHeight(player1, angle, speed).__str__())
        print('Treffer: ' + hit.__str__())
        print('')