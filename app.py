import colorsys
import random
WIDTH = 480
HEIGHT = 480

class Point:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def getPosition(self):
        return self.x, self.y
    
    def update(self):
        if self.vx == 0 and self.vy == 0:
            pass
        else:
            self.x += self.vx
            self.y += self.vy
            if (self.x > WIDTH and self.vx > 0) or (self.x < 0 and self.vx < 0):
                self.vx *= -1
            if (self.y > HEIGHT and self.vy > 0) or (self.y < 0 and self.vy < 0):
                self.vy *= -1        

class LinearCurve:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
    
    def t_func(self, t):
        ax, ay = self.pointA.getPosition()
        bx, by = self.pointB.getPosition()
        xt = ax * t + bx * (1-t)
        yt = ay * t + by * (1-t)
        return (xt, yt)
    
    def createNewLinearCurve(self, other, t):
        pointA = Point(*self.t_func(t))
        pointB = Point(*other.t_func(t))
        return LinearCurve(pointA, pointB)

class BezierCurve:
    def __init__(self, linearCurves):
        self.linearCurves = linearCurves
    
    def givePoints(self):
        points = []
        for T in range(100):
            t = T / 100
            linearCurves = self.linearCurves
            newLinearCurves = None

            while newLinearCurves is None or len(linearCurves) > 1:
                newLinearCurves = []
                for l in range(len(linearCurves)-1):
                    linearCurveA = linearCurves[l]
                    linearCurveB = linearCurves[l+1]
                    newLinearCurve = linearCurveA.createNewLinearCurve(linearCurveB, t)
                    newLinearCurves.append(newLinearCurve)
                linearCurves = newLinearCurves
            point = linearCurves[0].t_func(t)
            points.append(point)
        return points
    
    @classmethod
    def createFromPoints(cls, points):
        linearCurves = []
        for p in range(len(points)-1):
            linearCurve = LinearCurve(points[p], points[p+1])
            linearCurves.append(linearCurve)
        return cls(linearCurves)


if __name__ == '__main__':
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    s = pygame.Surface((WIDTH,HEIGHT))
    s.set_alpha(4)
    s.fill((0,0,0))

    rootPoint = Point(WIDTH/2, HEIGHT*1.03, 0, 0)

    points = [rootPoint]

    beziers = []
    for b in range(5):
        bpoints = [rootPoint]
        for p in range(3):
            x = random.randint(0, WIDTH-1)
            y = random.randint(0, HEIGHT-1)
            vx = random.randint(1,300) * random.choice([-0.001, 0.001])
            vy = random.randint(1,300) * random.choice([-0.001, 0.001])
            point = Point(x, y, vx, vy)
            bpoints.append(point)
        bezier = BezierCurve.createFromPoints(bpoints)
        beziers.append(bezier)
        points.extend(bpoints)

    while True:
        screen.blit(s, (0,0))
        for b, bezier in enumerate(beziers):
            rgb = tuple(round(i*255) for i in colorsys.hsv_to_rgb(0.4, 1, 1))
            pygame.draw.lines(screen, rgb, False, bezier.givePoints(), width=4)
        for event in pygame.event.get():
            pass
        pygame.display.update()
        for point in points:
            point.update()