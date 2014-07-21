# coding=utf-8
from idlelib.run import flush_stdout

__author__ = 'M'

import math
from ..utils.classes import *
from ..utils.gameconsts import Consts

class Calculation:

    def __init__(self, map_width, horizon, players, player_positions):
        self.__width = map_width
        self.__horizon = horizon
        self.__players = players
        self.__player_positions = player_positions

    @staticmethod
    def interpolate_point(x,point_0, point_1):
        diff_x = point_1.x - point_0.x
        delta_x = x - point_0.x
        if (diff_x != 0):
            result = Point(x, (point_0.y + (delta_x * float(point_1.y - point_0.y) / diff_x)))
        else:
            result = Point(x,(point_1.y + point_0.y) / 2) # sinnvollen Wert annehmen ?

        return result

    def calc_flugbahn(self, source, angle, speed):
        """
        Berechnet den Auftreffpunkt und die Zerstörung
        :param source: Player
        :param angle: Double
        :param power: Double
        :return: Flugbahn mit Hits
        mögl. Rückgabewerte in Hits:
            leer: nichts getroffen oder Horizont getroffen
            Hit[0..1]: Treffer der Targets
        """

        source_pos = self.__player_positions[source]

        flugbahn = self.__calc_flugbahn(source_pos, angle, speed)

        for player in self.__players:
            if not player is source:
                # Selbstabschuss nicht zulassen, macht einige Probleme
                hit = self.__calc_target_hit(flugbahn, player)
                flugbahn.setHit(hit)

        # Flugbahn kürzen, endet beim ersten Treffer!
        if len(flugbahn.hits) > 0:
            flugbahn.time_points = flugbahn.time_points[:int(flugbahn.hits[0].t / Consts.TIME_RESOLUTION)]
        return flugbahn

    def __is_horizon_hit(self, bullet_pos):
        # Horizonttreffer am Rand des Geschosses oder in doch erst in der Mitte ?
        # TODO: Horizonthöhe berechnen / interpolieren?
        return bullet_pos.y < self.__horizon[int(bullet_pos.x)]
        # return bullet_pos.y - Consts.BULLET_RADIUS < self.__horizon[int(round(bullet_pos.x))]

    def __calc_target_hit_percent(self, target_pos, bullet_pos):
        # kürzesten Abstand zwischen Ziel und Geschossmittelpunkt mit Pytagoras ermitteln
        distanceValue = math.hypot(target_pos.x - bullet_pos.x, target_pos.y - bullet_pos.y)

        distanceRadii = Consts.PLAYER_RADIUS + Consts.BULLET_RADIUS
        overlap = distanceRadii - distanceValue

        # Überlappung > 0 = Treffer
        if overlap > 0:
            # Überdeckung der Kreisradien als Maß für Treffer-% ermitteln
            # ggf. Flächeninhalt der Überdeckung als genaueres Treffermaß berechnen
            # Rückgabe %-genau
            # TODO ggf. mit Ableitung numerisch den Punkt größter Annäherung berechnen
            # formel wolfram alpha
            # Eingabe:
            # Reduce[2 v Cos[a] (-q + r + v x Cos[a]) + 2 (g x - v Sin[a]) (-m + p + 0.5 g x^2 - v x Sin[a]) == 0, {a, g, m, p, q, r, v, x}]
            #(a-pi)/(2 pi)(not element)Z, g!=0,   x = -(-54 g^4 q v cos(a)+54 g^4 r v cos(a)-54 g^3 v^3 sin^3(a)+54 g^3 v^3 sin(a)+sqrt(4 (-9 g^2 v^2 sin^2(a)-6 g^2 (g m-g p-v^2))^3+(-54 g^4 q v cos(a)+54 g^4 r v cos(a)-54 g^3 v^3 sin^3(a)+54 g^3 v^3 sin(a))^2))^(1/3)/(3 2^(1/3) g^2)+(2^(1/3) (-9 g^2 v^2 sin^2(a)-6 g^2 (g m-g p-v^2)))/(3 g^2 (-54 g^4 q v cos(a)+54 g^4 r v cos(a)-54 g^3 v^3 sin^3(a)+54 g^3 v^3 sin(a)+sqrt(4 (-9 g^2 v^2 sin^2(a)-6 g^2 (g m-g p-v^2))^3+(-54 g^4 q v cos(a)+54 g^4 r v cos(a)-54 g^3 v^3 sin^3(a)+54 g^3 v^3 sin(a))^2))^(1/3))+(v sin(a))/g
            return round(float(overlap) / distanceRadii, 2)
        else:
            return 0

    def __calc_target_hit(self, flugbahn, target):
        result = Hit(0,0,0,0,target)

        target_pos = self.__player_positions[target]

        # Rechteck um Ziel festlegen
        target_rect = Rect(Point(target_pos.x - Consts.PLAYER_RADIUS, target_pos.y + Consts.PLAYER_RADIUS),
                           Point(target_pos.x + Consts.PLAYER_RADIUS, target_pos.y - Consts.PLAYER_RADIUS))
        # abschussPhase = True
        for point in flugbahn.time_points:
            # if abschussPhase and math.hypot(point.x, point.y) > Consts.PLAYER_RADIUS:
            #     abschussPhase = False
            # zuerst grob prüfen, ob Zielrechteck getroffen wurde
            # (not abschussPhase) and
            if point.x > target_rect.topLeft.x and point.x <= target_rect.bottomRight.x and \
                point.y <= target_rect.topLeft.y and point.y >= target_rect.bottomRight.y:
                # X und Y des Geschosses im Zielrechteck, Treffer anhand der Umkreise genauer prüfen
                # Maximalwert zurückgeben
                hitPercent = self.__calc_target_hit_percent(target_pos, point)
                if result.percent < hitPercent:
                    result.x = point.x
                    result.y = point.y
                    result.t = point.t
                    result.percent = hitPercent

        if result.percent > 0:
            return result
        else:
            return None

    def __calc_flugbahn(self, source_pos, angle, speed):
        """
        Berechnet die Flugbahn bis zum ersten Treffer des Horizonts
        :param source_pos: Abschusspos. (Mitte Panzer)
        :param angle: Abschusswinkel (Radiant)
        :param speed: Abschussgeschwindigkeit (m/s)
        :return: Flugbahn(source_pos, time_points, targets = None)
        """
        result = Flugbahn(source_pos, TimePoint(0,0,0), [], list())

        t = Consts.TIME_RESOLUTION
        point = self.__calc_pos(t, source_pos, angle, speed)
        result.time_points.append(point)

        while int(point.x) < Consts.WORLD_WIDTH and (not self.__is_horizon_hit(point)):
            t += Consts.TIME_RESOLUTION
            point = self.__calc_pos(t, source_pos, angle, speed)
            if point.y > result.max_y_point.y:
                result.max_y_point = point
            result.time_points.append(point)

        return result

    def __calc_y(self, x, angle, speed):
        # TODO Formel prüfen!
        return x * math.tan(angle) - (Consts.g * math.pow(x,2))/(2* math.pow(speed,2) * math.pow(math.cos(angle),2)) # ohne Berücksichtigung Luftwiderstand

    def __calc_pos(self, t, source_pos, angle, speed):
        # ohne Berücksichtigung Luftwiderstand
        #v_x0=cos(phi)*v_0
        #v_y0=sin(phi)*v_0
        #s_x=v_x0 * t
        #s_y=v_y0*t-0.5*g*t^2
        #->
        #s_x = cos(phi)*v_0*t
        #s_y = sin(phi) * v_0 * t -0.5* g * t^2
        return TimePoint(source_pos.x + math.cos(angle) * speed * t, \
                     source_pos.y + math.sin(angle) * speed * t -0.5 * Consts.g * math.pow(t,2), \
                     t)
