import pygame
import math
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

vel_limit = 50
f_limit = 100

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Window runtime loop
win_loop = True

def magDir(x, y):
    return math.sqrt(x**2 + y**2), atan2(y, x)

def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

def mag(x, y):
    return math.sqrt(x**2 + y**2)

def setMag(x, y, m):
    
    magnitude = mag(x, y)
    
    if magnitude == 0:
        return 0, 0
    else:
    
        x = x/magnitude * m
        y = y/magnitude * m
    
    return x, y

def unitVector(x, y):
    x, y = setMag(x, y, 1)
    
    return x, y

def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

def distance(body1, body2):
    ## Difference in x-pos and y-pos
    delta_x = body2.px - body1.px
    delta_y = body2.py - body1.py
    
    ## Uses Pythagorean Theorem
    return math.sqrt((delta_x)**2 + (delta_y)**2)

class Body(object):
    def __init__(self, col, mass, p, v, a, f):
        self.col = col
        self.mass = mass
        self.radius = int(math.sqrt(mass) * 3)
        
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
    def changePos(self):
        
        self.px = int(self.px + self.vx)
        self.py = int(self.py + self.vy)
    
    def changeVel(self):
        self.vx += self.ax
        self.vy += self.ay
        
    def changeAcc(self):
        self.ax += self.fx/self.mass
        self.ay += self.fy/self.mass
    
class Attracter(Body):
    def __init__(self, G, p, col):
        self.G = G
        Body.__init__(self, col, 10, p, (0, 0), (0, 0), (0,0))
    
    def attract(self, body):
        
        r = distance(self, body)
        dir_x, dir_y = unitVector((self.px - body.px), (self.py-body.py))
        
        if r != 0:
            strength = self.G * (self.mass * body.mass) / r**2
        else:
            strength = 100
        
        fx, fy = setMag(dir_x, dir_y, strength)
        
        fx, fy = limit(fx, fy, f_limit)
        
        body.fx += fx
        body.fy += fy
        #print (body.fx, body.fy)

px = centre[0]
py = centre[1]

vx = 4
vy = 4

acc_val = 0.5
vel_limit = 15

def changePos(px, py, vx, vy):
    
    px += vx
    py += vy
    
    return px, py

def changeVel(vx, vy, ax, ay):
    vx += ax
    vy += ay
    
    return vx, vy
    


while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
        
    
    mouse = pygame.mouse.get_pos()
    
    accx = mouse[0] - px
    accy = mouse[1] - py
    
    accx, accy = setMag(accx, accy, acc_val)
    
    vx, vy = changeVel(vx, vy, accx, accy)
    
    print (limit(vx, vy, vel_limit))
    
    vx, vy = limit(vx, vy, vel_limit)
    
    
    if px+vx >= win_size[0] or px+vx < 0:
        vx = -vx
        
    if py+vy >= win_size[1] or py+vy < 0:
        vy = -vy
    
    px, py = changePos(px, py, vx, vy)
    
    #if px >= win_size[0] or px < 0 or py >= win_size[1] or py <= 0:
  #      px, py = px, py
        
    pygame.draw.circle(screen, (255, 100, 0), (int(px), int(py)), 20)

    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()