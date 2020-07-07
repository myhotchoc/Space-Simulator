import pygame, sys


# Defining Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

g = 9.8

def magDir(x, y):
    return math.sqrt(x**2 + y**2), atan2(y, x)

def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

def mag(x, y):
    return math.sqrt(x**2 + y**2)

def setMag(x, y, m):
    magnitude = mag(x, y)
    x = x/magnitude * m
    y = y/magnitude * m
    
    return x, y

def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

class Body(object):
    def __init__(self, col, mass, p, v, a, f, theta, ang_vel, ang_acc):
        self.col = col
        self.mass = mass
        
        self.size = (mass, mass)
        
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
    
    def changeAngAcc(self):
        self.ang_acc -= self.vx
    
    def changeAngVel(self):
        self.ang_vel += self.ang_acc
        
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
        
        self.changePos()
    
    def rotate(self):
        self.rect.center = (self.px, self.py)
        ## Make copy of old centre of rectangle
        self.old_centre = self.rect.center
        
        ## Angle of rotation
        self.theta = (self.theta + self.ang_vel) % 360
        
        ## Rotate original image
        self.new_image = pygame.transform.rotate(self.image_orig, self.theta)
        self.rect = self.new_image.get_rect()
        
        ## Set rotated image to old centre
        self.rect.center = self.old_centre
        
        ## Draw rotated image to screen
        screen.blit(self.new_image, self.rect)
    
    def moveToMouse(self, mouse):
        self.ax = mouse[0] - self.px
        self.ay = mouse[1] - self.py
        
        self.ax, self.ay = setMag(self.ax, self.ay, acc_val)
        
        self.changeVel()
        
        self.vx, self.vy = limit(self.vx, self.vy, vel_limit)
        self.changePos()
        

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

zero = (0, 0)

## Body = (colour, mass, pos, vel, acc, force, theta, ang_vel, ang_acc):

body1 = Body(BLUE, 100, (win_size[0]/3, centre[1]), zero, zero, zero, 0, 0, 0)
body2 = Body(RED, 100, (2*win_size[0]/3, centre[1]), zero, zero, zero, 0, 0, 0)

# ang_acc - negative=clockwise

bodies = [body1, body2]

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
        
        ## Angle of rotation
        i.changeAngAcc()
        i.changeAngVel()
        
        if i.ang_vel > ang_vel_lim:
            i.ang_vel = ang_vel_lim
        
        if i.ang_vel < -ang_vel_lim:
            i.ang_vel = -ang_vel_lim
            
        print (i.ang_vel)
        
        i.rotate()
        
        i.bounce()
        
        mouse = pygame.mouse.get_pos()
        i.moveToMouse(mouse)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()