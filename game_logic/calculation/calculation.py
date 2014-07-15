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

    def __init__(self, map_width, horizon, player_positions):
        self.__width = map_width
        self.__horizon = horizon
        self.__player_positions = player_positions

    def calcHit(self, source, target, angle, speed):
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
        flugbahn = self.__calc_flugbahn(source, angle, speed)
        hit_horizon_pos = self.__calc_horizon_hit_pos(flugbahn)
        hit_player = self.__calc_target_hit(flugbahn)

        if hit_player is None:
            return Hit(hit_horizon_pos.x, hit_horizon_pos.y, 0)
        else:
            return hit_player

    def calcHorizonHeight(self, source, angle, speed):
        """
        Berechnet die höchste Position der Flugbahn
        :param angle:
        :param speed:
        :return:
        """
        result = 0
        flugbahn = self.__calc_flugbahn(source, angle, speed)

        for y in flugbahn:
            result = max(result, y)

        return result

    def __calc_horizon_hit_pos(self, flugbahn):
        for x in xrange(self.__width):
            if flugbahn[x] <= self.__horizon[x]:
                return Point(x, flugbahn[x])
        return None

    def __calc_target_hit_percent(self, target_pos, bullet_pos):
        # X- und Y-Abstände ermitteln
        distance = Point(target_pos.x - bullet_pos.x, target_pos.y - bullet_pos.y)

        # kürzesten Abstand zwischen Ziel und Geschossmittelpunkt mit Pytagoras ermitteln
        distanceValue = math.sqrt(distance.x^2 + distance.y^2)

        # Überdeckung der Kreisradien als Maß für Treffer-% ermitteln
        # ggf. Flächeninhalt der Überdeckung als genaueres Treffermaß berechnen
        overlap = -1 * distanceValue - Consts.PLAYER_RADIUS - Consts.BULLET_RADIUS

        # Überlappung = Treffer
        if overlap > 0:
            return float(overlap) / Consts.PLAYER_RADIUS
        else:
            return 0

    def __calc_target_hit(self, flugbahn, target_pos):
        result = Hit(0,0,0)

        # Rechteck um Ziel festlegen
        target_rect = Rect(Point(target_pos.x - Consts.PLAYER_RADIUS, target_pos.y - Consts.PLAYER_RADIUS),
                           Point(target_pos.x + Consts.PLAYER_RADIUS, target_pos.y + Consts.PLAYER_RADIUS))
        for x in xrange(self.__width):
            # zuerst grob prüfen, ob Zielrechteck getroffen wurde
            if x > target_rect.topLeft.x and x <= target_rect.bottomRight.x and \
                flugbahn[x] >= target_rect.topLeft.y and flugbahn[x] <= target_rect.bottomRight.y:
                # X und Y des Geschosses im Zielrechteck, Treffer anhand der Umkreise genauer prüfen
                # Maximalwert zurückgeben
                hitPercent = self.__calc_target_hit_percent(Point(x, flugbahn[x]))
                if result.percent < hitPercent:
                    result.x = x
                    result.y = flugbahn[x]
                    result.percent = hitPercent

        if result.percent > 0:
            return result
        else:
            return None

    def __calc_flugbahn(self, source, angle, speed):
        result = []
        y_offset = self.__player_positions[source]
        w = self.__width

        for x in xrange(w):
            result.append(y_offset + self.__calc_y(x, angle, speed))

        return result

    def __calc_y(self, x, angle, speed):
        return x * math.tan(angle) - (math.g * x^2)/(2* speed^2 * math.cos(angle)^2) # ohne Berücksichtigung Luftwiderstand

