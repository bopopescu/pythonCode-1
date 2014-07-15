from __builtin__ import bool

__author__ = 'M'
# coding=utf-8

class Point:
    # x = 0
    # y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

class Hit(Point):
    def __init__(self, x, y, percent):
        self.x = x
        self.y = y
        self.percent = percent

class Rect:
    topLeft = Point(x=0, y=0)
    bottomRight = Point(x=0, y=0)

    def __init__(self, top_left, bottom_right):
        self.topLeft = top_left
        self.bottomRight  = bottom_right
