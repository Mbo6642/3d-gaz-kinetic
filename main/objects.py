
class Vector:
    def __init__(self, values):
        self.values = values
        self.size = len(values)

    def __rmul__(self, scalar):
        return Vector(
            [scalar * self.values[i] for i in range(self.size)]
        )

    def __add__(self, vec):
        return Vector(
            [self.values[i] + vec.values[i] for i in range(self.size)]
        )
    
    def __sub__(self, vec):
        return Vector(
            [self.values[i] - vec.values[i] for i in range(self.size)]
        )

    def dot(self, vec):
        return sum(self.values[i]*vec.values[i] for i in range(self.size))

    def norm(self):
        return self.dot(self) ** .5
    
    def normalize(self):
        return 1/self.norm() * self
    
    def project(self, vec):
        return self.dot(vec)/self.dot(self) * self
    
    def r2(self):
        return Vector(self.values[:2])
    
    def cross(self, vec):
        return Vector(
            [
                self.values[(1 + i) % 3] * vec.values[(2 + i) % 3] -
                self.values[(2 + i) % 3] * vec.values[(1 + i) % 3]
                for i in range(3)
            ]
        )
    

class Plane:
    def __init__(self, normal_vec):
        self.normal_vec = normal_vec

    def orth_project(self, pnt):
        return self.normal_vec + pnt - self.normal_vec.project(pnt)
    
    def persp_project(self, pnt):
        return self.normal_vec.dot(self.normal_vec)/self.normal_vec.dot(pnt) * pnt
    

class Ball:

    constant_radius = False 
    dt = .005
    balls = []

    def __init__(self, center, spd_vec, radius=1, mass=1):
        self.center = Vector(center)
        self.spd_vec = Vector(spd_vec)
        self.radius = radius
        self.mass = mass

        Ball.balls.append(self)

    
    def updt_pos(self):
        self.center += Ball.dt * self.spd_vec

    def collision(self, other):
        return (self.center - other.center).norm() < self.radius + other.radius
    
    def collide(self, other):
        dir_vector = other.center - self.center

        r1 = self.mass/(self.mass + other.mass)
        r2 = other.mass/(self.mass + other.mass)

        u1 = dir_vector.project(self.spd_vec)
        w1 = self.spd_vec - u1

        u2 = dir_vector.project(other.spd_vec)
        w2 = other.spd_vec - u2

        v1 = (r1 - r2)*u1 + 2*r2*u2
        v2 = (r2 - r1)*u2 + 2*r1*u1

        self.spd_vec = v1 + w1
        other.spd_vec = v2 + w2

    def updt_spd_vec():
        for i, ball1 in enumerate(Ball.balls):
            for ball2 in Ball.balls[i + 1:]:
                if ball1.collision(ball2):
                    ball1.collide(ball2)
    def updt():
        for ball in Ball.balls:    
            ball.updt_pos()


class Border:

    borders = []

    def __init__(self, normal_vec, size):
        self.plane = Plane(normal_vec)
        self.size = size

        self.coll_cnt = 0

        self.corners = [
            [1, 1, 1],
            [1, 1, 2],
            [1, -1, 2],
            [1, -1, 1],
        ]

        Border.borders.append(self)

    def distance(self, pnt):
        return (pnt - self.plane.orth_project(pnt)).norm()
    
    def collision(self, ball):
        return self.distance(ball.center) < ball.radius
    
    def collide(self, ball):
        ball.spd_vec -= 2*self.plane.normal_vec.project(ball.spd_vec)
        self.coll_cnt += 1
        print(self.coll_cnt)
        
    def updt():
        for border in Border.borders:
            for ball in Ball.balls:
                if border.collision(ball):
                    border.collide(ball)
