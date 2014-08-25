#coding=utf-8
__author__ = 'M'

import random

from model.match import Match
from utils.gameconsts import Consts
from utils.classes import Point
from calculation.calculation import Calculation

class MatchBuilder:
    f_random = random

    @staticmethod
    def __get_new_horizon_skeleton(world_width):
        MatchBuilder.f_random.seed()

        MAX_LOOPS = 9000
        num_loops = 0
        points = []
        points_count = MatchBuilder.f_random.randint(Consts.MIN_SAMPLING_POINTS, Consts.MAX_SAMPLING_POINTS)

        points.append(Point(0, MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT, Consts.MAX_HORIZON_HEIGHT)))
        points.append(Point(world_width - 1, MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT, Consts.MAX_HORIZON_HEIGHT)))

        max_x = world_width - 2

        while len(points) < points_count  and num_loops < MAX_LOOPS:
            num_loops += 1
            points.append(Point(MatchBuilder.f_random.randint(1, max_x),
                          MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT,
                                                        Consts.MAX_HORIZON_HEIGHT)))

            points.sort(key= lambda point: point.x)

            start_point = points[0]
            for point in points[1::]:
                if point.x == start_point.x:
                    points.remove(point)
                else:
                    c = abs(Calculation.derivation(start_point, point))
                    if c > Consts.MAX_DERIVATION:
                        if point.x > (max_x): #Endpunkt nicht löschen ?!
                            points.remove(start_point)
                        else:
                            points.remove(point)
                    else:
                        start_point = point

        return points

    @staticmethod
    def __get_new_player_x_positions(players, world_width):
        result = []

        # etwas übertrieben kompliziert, evtl. können mehr als 2 Player spielen?
        parts_width = float(world_width) / (len(players) + 1)
        for i in xrange(len(players)):
            if (i < len(players) / 2):
                result.append(int(max(round(i * parts_width + Consts.PLAYER_RADIUS +
                    ((parts_width-2* Consts.PLAYER_RADIUS) * MatchBuilder.f_random.random()))-1,0)))
            else:
                result.append(int(max(round((i + 1) * parts_width + Consts.PLAYER_RADIUS +
                    ((parts_width-2* Consts.PLAYER_RADIUS ) * MatchBuilder.f_random.random()))-1,0)))

        return result

    @staticmethod
    def get_match(players):
        """
        Erstellt ein neues Match, setzt es für die Spieler
        müsste auch die Spieler erzeugen?
        :rtype : Match
        """
        MatchBuilder.f_random.seed()
        world_width = Consts.WORLD_WIDTH

        player_order = range(len(players))
        MatchBuilder.f_random.shuffle(player_order)
        ordered_players = []
        for i in player_order:
            ordered_players += [players[i]]

        match = Match(ordered_players, world_width, MatchBuilder.__get_new_horizon_skeleton(world_width),
                      MatchBuilder.__get_new_player_x_positions(players, world_width))

        for player in players:
            player.setMatch(match)

        return match

