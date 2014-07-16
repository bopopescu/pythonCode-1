__author__ = 'M'

import math

from game_logic.match_builder import MatchBuilder
from game_logic.model.player import Player
from game_logic.model.match import Match

if __name__ == '__main__':
    player1 = Player(0,0)
    player2 = Player(1,1)

    for i in xrange(1000):
        testMatch = MatchBuilder.get_match([player1, player2])
        angle = math.pi / 4
        speed = 60
        hit = testMatch.calcHit(player1, angle, speed)
        print(player1)
        print(player2)
        print(testMatch)
        print(testMatch.calculation.calcHorizonHeight(player1, angle, speed))
        print(hit)