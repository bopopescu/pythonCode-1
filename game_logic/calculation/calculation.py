# coding=utf-8
__author__ = 'M'

import math
from ..utils.classes import *
from ..utils.gameconsts import Consts

class Calculation:
    # __horizon = []
    # __height = 0
    # __width = 0
    # __player_radius = 0
    # __player_positions = []

    def __init__(self, map_width, horizon, players, player_positions):
        self.__width = map_width
        self.__horizon = horizon
        self.__players = players
        self.__player_positions = player_positions

    def calcHit(self, source, angle, speed):
        """
        Berechnet den Auftreffpunkt und die Zerstörung
        :param source: Player
        :param target: Player
        :param angle: Double
        :param power: Double
        :return: Hit
        mögl. Rückgabewerte:
            None: nichts getroffen - bleibt in der Luft?
            Hit: Treffer Horizontlinie (percent = 0) oder Target (percent > 0)
        """
        result = None
        source_pos = self.__player_positions[source]
        flugbahn = self.__calc_flugbahn(source_pos, angle, speed)

        for player in self.__players:
            # TODO: für Treffer mehrerer Ziele anpassen?
            # berechnet z.Zt. nur für ersten Treffer
            result = self.__calc_target_hit(flugbahn, player)
            if result:
                break

        if result is None:
            result = self.__calc_horizon_hit(flugbahn)

        return result

    def calcHorizonHeight(self, source, angle, speed):
        """
        Berechnet die höchste Position der Flugbahn
        :param angle:
        :param speed:
        :return:
        """
        result = 0
        source_pos = self.__player_positions[source]
        flugbahn = self.__calc_flugbahn(source_pos, angle, speed)

        for point in flugbahn:
            result = max(result, point.y)

        return result

    def __calc_horizon_hit(self, flugbahn):
        result = None

        for point in flugbahn:
            last_point = point
            if not point is flugbahn[0]:
                if point.y - Consts.BULLET_RADIUS < self.__horizon[point.x]:
                    # TODO Flugbahn.slice
                    result = Hit(flugbahn,last_point.x, self.__horizon[point.x])

        return result

    def __calc_target_hit_percent(self, target_pos, bullet_pos):
        # X- und Y-Abstände ermitteln
        distance = Point(target_pos.x - bullet_pos.x, target_pos.y - bullet_pos.y)

        # kürzesten Abstand zwischen Ziel und Geschossmittelpunkt mit Pytagoras ermitteln
        distanceValue = math.sqrt(math.pow(distance.x,2) + math.pow(distance.y,2))

        # Überdeckung der Kreisradien als Maß für Treffer-% ermitteln
        # ggf. Flächeninhalt der Überdeckung als genaueres Treffermaß berechnen
        overlap = -1 * distanceValue - Consts.PLAYER_RADIUS - Consts.BULLET_RADIUS

        # Überlappung = Treffer
        if overlap > 0:
            return float(overlap) / Consts.PLAYER_RADIUS
        else:
            return 0

    def __calc_target_hit(self, flugbahn, target):
        result = Hit(flugbahn,0,0,0,target)
        target_pos = self.__player_positions[target]

        # Rechteck um Ziel festlegen
        target_rect = Rect(Point(target_pos.x - Consts.PLAYER_RADIUS, target_pos.y - Consts.PLAYER_RADIUS),
                           Point(target_pos.x + Consts.PLAYER_RADIUS, target_pos.y + Consts.PLAYER_RADIUS))
        for point in flugbahn:
            # zuerst grob prüfen, ob Zielrechteck getroffen wurde
            if point.x > target_rect.topLeft.x and point.x <= target_rect.bottomRight.x and \
                point.y >= target_rect.topLeft.y and point.y <= target_rect.bottomRight.y:
                # X und Y des Geschosses im Zielrechteck, Treffer anhand der Umkreise genauer prüfen
                # Maximalwert zurückgeben
                hitPercent = self.__calc_target_hit_percent(target_pos, point)
                if result.percent < hitPercent:
                    result.x = point.x
                    result.y = point.y
                    result.percent = hitPercent

        if result.percent > 0:
            return result
        else:
            return None

    def __calc_flugbahn(self, source_pos, angle, speed):
        result = []
        w = self.__width - source_pos.x

        for x in xrange(w):
            result.append(Point(source_pos.x + x, source_pos.y + Consts.PLAYER_RADIUS + self.__calc_y(x, angle, speed))) # Abschusshöhe. in der Mitte des Spielers?

        return result

    def __calc_y(self, x, angle, speed):
        #TODO Formel prüfen!
        return x * math.tan(angle) - (Consts.g * math.pow(x,2))/(2* math.pow(speed,2) * math.pow(math.cos(angle),2)) # ohne Berücksichtigung Luftwiderstand

