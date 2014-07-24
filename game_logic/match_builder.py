# coding=utf-8
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
        points_count = MatchBuilder.f_random.randint(Consts.MIN_SAMPLING_POINTS, Consts.MAX_SAMPLING_POINTS)

        points = []
        points.append(Point(0,
                      MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT, Consts.MAX_HORIZON_HEIGHT)))
        points.append(Point(world_width - 1,
                      MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT, Consts.MAX_HORIZON_HEIGHT)))

        # ist GAP_TO_FIRST_SAMPLING_POINT notwendig?
        # TODO: an allen Stützpunkten GAP_TO_FIRST_SAMPLING_POINT berücksichtigen!
        max_x = world_width - 1 - Consts.GAP_TO_FIRST_SAMPLING_POINT
        for i in xrange(points_count-2):
            points.append(Point(MatchBuilder.f_random.randint(Consts.GAP_TO_FIRST_SAMPLING_POINT, max_x),
                          MatchBuilder.f_random.randint(Consts.MIN_HORIZON_HEIGHT, Consts.MAX_HORIZON_HEIGHT)))

        points.sort(key= lambda point: point.x)

        #TODO Random wieder aktivieren
        points = [Point(0,0), Point(100,100), Point(500,100), Point(world_width-1, 0)]

        return points

    @staticmethod
    def __get_new_player_x_positions(players, world_width):
        result = []

        # etwas übertrieben kompliziert, evtl. können mehr als 2 Player spielen?
        parts_width = float(world_width) / (len(players) + 1)
        for i in xrange(len(players)):
            if (i < len(players) / 2):
                result.append(int(max(round(i * parts_width + (parts_width * MatchBuilder.f_random.random()))-1,0)))
            else:
                result.append(int(max(round((i + 1) * parts_width + (parts_width * MatchBuilder.f_random.random()))-1,0)))

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
        match = Match(players, world_width, MatchBuilder.__get_new_horizon_skeleton(world_width), MatchBuilder.__get_new_player_x_positions(players, world_width))

        for player in players:
            player.match = match

        return match
