from objects import *

def sphere_projection(ball, plane):
    C = (1 - ball.radius**2 / ball.center.norm() ** 2) * ball.center
    r = (ball.radius**2 - ball.radius**4 / ball.center.norm() ** 2) ** 0.5

    polar_plane = Plane(C)
    X = polar_plane.persp_project(plane.normal_vec)
    v = (X - C).normalize()
    u = v.cross(X).normalize()

    P1, P2 = C - r * v, C + r * v
    Q1, Q2 = plane.persp_project(P1), plane.persp_project(P2)

    M = 0.5 * (Q1 + Q2)
    N = polar_plane.persp_project(M)

    P3 = N + ((r**2 - (C - N).norm() ** 2) ** 0.5) * u
    Q3 = plane.persp_project(P3)

    return M.r2(), (Q1 - M).r2(), (Q3 - M).r2()

