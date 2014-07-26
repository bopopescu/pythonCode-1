# coding=utf-8
from Tkinter import *
from game_logic.model.player import *
from game_logic.model.match import *
from game_logic.match_builder import *


import math

fenster = Tk()
height = 400
width = 600
flaeche = Canvas(fenster, width=width, height=height)

def zeichnen():
    player1 = Player('A',None)
    player2 = Player('B',None)

    testMatch = MatchBuilder.get_match([player1, player2])
    print(testMatch)

    # for i in xrange(5):
    angle = math.pi / 4
    speed = 200
    flugbahn = testMatch.calc_flugbahn(player1, angle, speed)
    print('letzter Punkt: ' + flugbahn.time_points[len(flugbahn.time_points)-1].__str__())
    print('Schusshöhe: {:.2f}'.format(flugbahn.max_y_point.y))
    for hit in flugbahn.hits:
        print('Treffer: ' + hit.__str__())
    print('')

    flaeche.delete(ALL)

    start_point = testMatch.horizon[0]
    for point in testMatch.horizon[1::]:
        flaeche.create_line(start_point.x, height - start_point.y, point.x, height - point.y)
        start_point = point

    point = testMatch.getPlayerPostion(player1)
    flaeche.create_rectangle(point.x - Consts.PLAYER_RADIUS, height - point.y - Consts.PLAYER_RADIUS,
                             point.x + Consts.PLAYER_RADIUS, height - point.y + Consts.PLAYER_RADIUS, fill="blue")

    point = testMatch.getPlayerPostion(player2)
    flaeche.create_rectangle(point.x - Consts.PLAYER_RADIUS, height - point.y - Consts.PLAYER_RADIUS,
                             point.x + Consts.PLAYER_RADIUS, height - point.y + Consts.PLAYER_RADIUS, fill="red")
# s = eingabe.get()
#     for i in range(4000):
#         x = i/200.0 - 10
#         f = eval(s)
#         flaeche.create_line(x*20+200,200-f*20,x*20+201,200-f*20)

# eingabe = Entry(fenster, width=40)
# label = Label(fenster, text='f(x)=')
button = Button(fenster,text='zeichnen',command=zeichnen)
flaeche.pack()
# label.pack(side=LEFT)
# eingabe.pack(side=LEFT)
button.pack(side=RIGHT,pady=10,padx=10)

zeichnen()

# flaeche.create_line(200,0,200,400)

fenster.mainloop()