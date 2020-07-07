import pygame, sys


# Defining Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

g = 9.8

def magDir(x, y):
    return math.sqrt(x**2 + y**2), atan2(y, x)

def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

def mag(x, y):
    return math.sqrt(x**2 + y**2)

def setMag(x, y, m):
    magnitude = mag(x, y)
    if magnitude != 0:
        x = x/magnitude * m
        y = y/magnitude * m
    
    else:
        x = 0
        y = 0
    
    return x, y

def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

def distance(body1, body2):
    
    print (type(body1), type(body2))
    ## Difference in x-pos and y-pos
    delta_x = body2.px - body1.px
    delta_y = body2.py - body1.py
    
    ## Uses Pythagorean Theorem
    return math.sqrt((delta_x)**2 + (delta_y)**2)

class Body(object):
    def __init__(self, col, mass, p, v, a, f, theta, ang_vel, ang_acc):
        self.col = col
        self.mass = mass
        
        self.size = (mass, mass)
        self.radius = int(math.sqrt(mass) * 3)
        
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
        self.theta = theta
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc
        
        self.weight = [0, self.mass * g]
        
        ## Defining surface (rectangle)
        self.image_orig = pygame.Surface(self.size)
        ## Makes background transparent
        self.image_orig.set_colorkey(BLACK)
        
        ## Fill rectangle colour
        self.image_orig.fill(self.col)
        
        ## Create copy of original image (makes it smoother?)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        
        ## Rect object (holds position)
        self.rect = self.image.get_rect()
        
    
    def changePos(self):
        
        self.px = int(self.px + self.vx)
        self.py = int(self.py + self.vy)
    
    def changeVel(self):
        self.vx += self.ax
        self.vy += self.ay
        
    def changeAcc(self):
        self.ax += self.fx/self.mass
        self.ay += self.fy/self.mass
        
    def applyForce(self, force):
        self.fx += force[0]
        self.fy += force[1]
        #print (self.fy)
    
        
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
        
        self.changePos()
    
    
    def moveToMouse(self, mouse):
        self.ax = mouse[0] - self.px
        self.ay = mouse[1] - self.py
        
        self.ax, self.ay = setMag(self.ax, self.ay, acc_val)
        
        self.changeVel()
        
        self.vx, self.vy = limit(self.vx, self.vy, vel_limit)
        self.changePos()
    
    
class Attracter(Body):
    def __init__(self, G, p, col):
        self.G = G
        Body.__init__(self, col, 10, p, (0, 0), (0, 0), (0,0), (0, 0), (0, 0), (0, 0))
    
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

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

acc_val = 0.5
vel_limit = 10
ang_vel_lim = 100
f_limit = 100

zero = (0, 0)

## Body = (colour, mass, pos, vel, acc, force, theta, ang_vel, ang_acc):

body1 = Body(BLUE, 100, (win_size[0]/3, centre[1]), (1, 0.5), zero, zero, 0, 0, 0)
body2 = Body(RED, 100, (2*win_size[0]/3, centre[1]), (0, -5), zero, zero, 0, 0, 0)
a1 = Attracter(300, centre, WHITE)

# ang_acc - negative=clockwise

bodies = [body1]

## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
   
    
    
    for i in bodies:
        
        a1.attract(i)      
        pygame.draw.circle(screen, a1.col, (a1.px, a1.py), a1.radius)
        
        i.ax, i.ay = 0, 0
        #i.fx, i.fy = 0, 0
        
        i.changeAcc()
        #i.ax, i.ay = setMag(i.ax, i.ay, 0.5)
        i.changeVel()
        
        i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        
        
        i.changePos()
        i.bounce()
    
        
        pygame.draw.circle(screen, i.col, (int(i.px), int(i.py)), i.radius)
        
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()