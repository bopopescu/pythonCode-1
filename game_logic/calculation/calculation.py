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
        source_pos = self.__player_positions[source]
        flugbahn = self.__calc_flugbahn(source_pos, angle, speed)
        hit_horizon_pos = self.__calc_horizon_hit_pos(flugbahn)
        hit_player = self.__calc_target_hit(flugbahn, self.__player_positions[target])

        if hit_player is None:
            if hit_horizon_pos:
                return Hit(hit_horizon_pos.x, hit_horizon_pos.y, 0)
            else:
                return None
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
        source_pos = self.__player_positions[source]
        flugbahn = self.__calc_flugbahn(source_pos, angle, speed)

        for point in flugbahn:
            result = max(result, point.y)

        return result

    def __calc_horizon_hit_pos(self, flugbahn):
        for point in flugbahn:
            last_point = point
            if not point is flugbahn[0]:
                if point.y - Consts.BULLET_RADIUS < self.__horizon[point.x]:
                    return Point(last_point.x, self.__horizon[point.x])
        return None

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

    def __calc_target_hit(self, flugbahn, target_pos):
        result = Hit(0,0,0)

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
        return x * math.tan(angle) - (Consts.g * math.pow(x,2))/(2* math.pow(speed,2) * math.pow(math.cos(angle),2)) # ohne Berücksichtigung Luftwiderstand

