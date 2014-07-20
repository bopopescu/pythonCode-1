__author__ = 'M'
# coding=utf-8

class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%i, %i)" % (self.x, self.y)

class TimePoint(Point):

    def __init__(self,x,y,t):
        Point.__init__(self,x, y)
        self.t = t

    def __str__(self):
        return Point.__str__() + '; t={:n}'.format(self.t)

class Hit(Point):
    def __init__(self, x, y, t, percent = 0, target = None):
        self.x = x
        self.y = y
        self.t = t
        self.percent = percent
        self.target = target

    def __str__(self):
        return Point.__str__(self) + '; damage={:.2f}%'.format(self.percent * 100)

class Rect:
    topLeft = Point(x=0, y=0)
    bottomRight = Point(x=0, y=0)

    def __init__(self, top_left, bottom_right):
        self.topLeft = top_left
        self.bottomRight  = bottom_right

class Flugbahn:
    def __init__(self, start_point, max_y_point = TimePoint(0,0,0), time_points = [], hits = list()):
        self.start_point = start_point
        self.time_points = time_points
        self.max_y_point = max_y_point
        self.hits = hits

    def setHit(self, hit):
        if hit:
            add = False
            for lHit in self.hits:
                if lHit.t > hit.t:
                    add = True
                    self.hits.remove(lHit)
                elif lHit.t == hit.t:
                    add = True

            if add or len(self.hits)==0:
                self.hits.append(hit)
