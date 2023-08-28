from objects import *
from math import sin, cos, pi
import turtle
from time import sleep
from sphere_projection import sphere_projection

def ellipse(center, vec1, vec2, pen, steps=80):
    pen.up()
    pen.goto((center + vec1).values)
    pen.down()

    angle = 0
    while angle < 2.1 * pi:
        pen.goto((center + cos(angle) * vec1 + sin(angle) * vec2).values)
        angle += 2 * pi / steps

    pen.up()


def render_ball(ball, zoom, rend_plane, pen):
    center, vec1, vec2 = sphere_projection(ball, rend_plane)
    ellipse(zoom*center, zoom*vec1, zoom*vec2, pen)


def render_border(border, zoom, rend_plane, pen):
    rend_corners = [
        rend_plane.persp_project(Vector(border.corners[i])).r2()
        for i in range(4)
    ]

    pen.up()
    pen.goto((zoom*rend_corners[-1]).values)
    pen.down()

    for i in range(4):
        pen.goto((zoom*rend_corners[i]).values)

    pen.up()


rend_plane = Plane(Vector([0, 0, .5]))

Ball([0.3, -.01, 1.8], [0, 1, 5], .07, 1000)

Ball([-0.3, -.01, 1.45], [0, 6, 2], .1, 1000)

Ball([-0.7, -.01, 1.10], [0, 1, 2], .07, 1000)

Ball([-0.7, -.7, 1.1], [1, 1, 1], .07, 1000)




win = turtle.Screen()
win.setup(1000, 1000)
win.tracer(0)

bg = turtle.Turtle(visible=False)
bg.color("black")
bg.up()

render_border(Border(Vector([1, 0, 0]), 10), 1000, rend_plane, bg)
Border(Vector([-1, 0, 0]), 10)
Border(Vector([0, 1, 0]), 10)
Border(Vector([0, -1, 0]), 10)
Border(Vector([0, 0, 1]), 10)
Border(Vector([0, 0, 2]), 10)

pen = turtle.Turtle(visible=False)
pen.color("black")
pen.up()


while True:

    Ball.updt_spd_vec()
    Border.updt()
    Ball.updt()

    pen.clear()
    pen.up()

    for ball in Ball.balls:
        render_ball(ball, 1000, rend_plane, pen)
        # print(b.center.values)


    win.update()
    sleep(Ball.dt)
