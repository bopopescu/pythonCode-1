from __builtin__ import bool

__author__ = 'M'
# coding=utf-8

class Point:
    # x = 0
    # y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x={:n}; y={:n}'.format(self.x, self.y)

class Hit(Point):
    def __init__(self, x, y, percent):
        self.x = x
        self.y = y
        self.percent = percent

    def __str__(self):
        return 'x={:n}; y={:n}, damage={:.2f}%'.format(self.x, self.y, self.percent * 100)

class Rect:
    topLeft = Point(x=0, y=0)
    bottomRight = Point(x=0, y=0)

    def __init__(self, top_left, bottom_right):
        self.topLeft = top_left
        self.bottomRight  = bottom_right

class Flugbahn:
    def __init__(self, x_start = 0, y_points = []):
        self.x_start = x_start
        self.y_points = y_points