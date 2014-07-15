__author__ = 'M'

import math

from game_logic.match_builder import MatchBuilder
from game_logic.model.player import Player
from game_logic.model.match import Match

if __name__ == '__main__':
    player1 = Player(0,0)
    player2 = Player(1,1)

    testMatch = MatchBuilder.get_match([player1, player2], 600)
    hit = testMatch.calcHit(player1, math.pi / 4, 200)
    print(hit)