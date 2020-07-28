# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 05:48:45 2020

@author: Danny
"""
import pygame, sys, math, random
from Box2D import *

## Colours
RED = [255, 0, 0, 255]
GREEN = [0, 255, 0, 255]
BLUE = [0, 0, 255, 255]
ORANGE = [255, 128, 0, 255]
YELLOW = [242, 224, 63, 255]
BLACK = [0, 0, 0, 255]
WHITE = [255, 255, 255, 255]
LIGHT_BLUE = [0,  255, 255, 255]
PINK = [255, 153, 255, 255]
LIME = [128, 255, 0, 255]

rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))


decay_speed = 1
lifespan = 25500
scale_factor = 1.655
grav = b2Vec2(0, 100)


## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

def convertCoordsToBox2D(x, y):
    new_x = (x-centre[0])
    new_y = (y-centre[1])
    
    return (new_x, new_y)

def convertCoordsToPygame(x, y):
    new_x = (x+centre[0])
    new_y = (y+centre[1])
    
    return new_x, new_y

class Box(object):
    def __init__(self, mass, pos, lifespan):
        self.mass = mass
        self.lifespan = lifespan
        
        self.col = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        
        self.theta = 0
        
        self.px = int(pos[0])
        self.py = int(pos[1])
        
        ## Defining surface (rectangle)
        self.image_orig = pygame.Surface((self.mass, self.mass)) 
        ## Makes background transparent
        self.image_orig.set_colorkey(BLACK)
        
        ## Fill rectangle colour
        self.image_orig.fill(self.col)
        
        ## Create copy of original image (makes it smoother?)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        
        ## Rect object (holds position)
        self.rect = self.image.get_rect()
        
# =============================================================================
#         bodyDef = b2BodyDef()
#         bodyDef.type = b2_dynamicBody
#         bodyDef.position = b2Vec2(mouse[0], mouse[1])
#         
#         self.body = world.CreateBody(bodyDef)
#         boxShape = b2PolygonShape(box=b2Vec2(self.mass, self.mass))
#         boxFixtureDef = b2FixtureDef(shape=boxShape)
#         boxFixtureDef.density = 1
#         boxFixtureDef.restitution = 0.3
#         self.body.createFixture(boxFixtureDef)
# =============================================================================
        
        start_pos_x, start_pos_y = convertCoordsToBox2D(mouse[0], mouse[1])
        
        self.body = world.CreateDynamicBody(position=b2Vec2(start_pos_x, start_pos_y),
                                            linearDamping=random.randint(0, 20))
                                           
        new_mass = self.mass / scale_factor
    
        self.box = self.body.CreatePolygonFixture(box=b2Vec2(new_mass, new_mass), density=1,
                                 friction=0.3)
    
    def updatePos(self):
        
        self.px, self.py = convertCoordsToPygame(self.body.position[0], self.body.position[1])
        self.theta += -self.body.angle
        
        #print (self.theta)
        
        #self.px = self.body.position[0]
        #self.py = self.body.position[1]
        
    def rotate(self):
        
        
        
        self.rect.center = (self.px, self.py)
        ## Make copy of old centre of rectangle
        self.old_centre = self.rect.center
        

        ## Rotate original image
        self.new_image = pygame.transform.rotate(self.image_orig, self.theta)
        self.rect = self.new_image.get_rect()
        
        ## Set rotated image to old centre
        self.rect.center = self.old_centre
        #self.image_orig.set_colorkey(self.col)
        
    
    def draw(self):
        #pygame.draw.rect(screen, self.col, (self.px, self.py, self.mass, self.mass))
        ## Draw rotated image to screen
        screen.blit(self.new_image, self.rect)
        
    ## Changes colour of particle - decrements RGB values
    def fade(self):
        for r in range(len(self.col)):
            #print (r, particle.col[r])
            if self.col[r] > decay_speed:
                self.col[r] = self.col[r] - decay_speed
            else:
                self.col[r] = decay_speed
        
        self.image_orig.fill(self.col)
    
    ## Check if still alive (using lifespan value)
    def isAlive(self):
        if self.lifespan <= 0:
            return False
        else:
            return True


## World manages sim, stores all elements
## Create box2d world with gravity set, and sleep to True
world = b2World(gravity=grav, doSleep=True)

def makeGroundShapeLong():
    
    ## 1. Create body definition - pos, type
    ## 2. Create body
    ## 3. Create shape
    ## 4. Create fixture
    
    ## 1
    ## Creating body definition, default is static
    ## Static - no mass, cannot move (platforms, etc)
    ## Dynamic - 'fully simulated', experiences forces, collisions
    ## Kinematic - moved manually, eg user-controlled - no collisions with statics or kinematics
    groundBodyDef = b2BodyDef()
    
    ## Setting bodyDef position
    groundBodyDef.position = b2Vec2(0, -10)

    ## 2
    ## Creating body, giving new defintion
    groundBody = world.CreateBody(groundBodyDef)
    
    ## 3
    ## Creating shape, giving box geometry
    groundBox = b2PolygonShape(box=b2Vec2(50, 10))
    
    ## 4
    ## Creating fixture definition attached to new shape
    groundBoxFixture = b2FixtureDef(shape=groundBox)
    
    ## Creating fixture on body
    groundBody.CreateFixture(groundBoxFixture)

#def makeGroundShapeShort():

# =============================================================================
# groundBody = world.CreateStaticBody(
#         position=b2Vec2(0, -10),
#         shapes=b2PolygonShape(box=b2Vec2(50,10)),
#         )
# 
# #def makeDynamicBody():
#     
# body = world.CreateDynamicBody(position=b2Vec2(0,4))
# 
# box = body.CreatePolygonFixture(box=b2Vec2(1, 1), density=1,
#                                 friction=0.3)
# =============================================================================
    
    

#makeGroundShapeLong()
#makeDynamicBody()

timeStep = 1.0/60

vel_iters, pos_iters = 6, 2



boxes = []
drawing = False

## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill(BLACK)
    
    
    b2World.Step(world, timeStep, vel_iters, pos_iters)
    
    b2World.ClearForces(world)

    
    
    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
        if i.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        
        if i.type == pygame.MOUSEBUTTONUP:
            drawing = False
            
    if drawing:
   #     b = Box(random.randint(15, 35), mouse)
        b = Box(25, mouse, lifespan)
        boxes.append(b)
        
    
    for i in boxes:
        i.updatePos()
        i.rotate()
        i.draw()
        i.lifespan -= decay_speed
        #i.fade()
        
        #print (i.lifespan)
        if i.lifespan < 0:
            print (4444444)
            boxes.remove(i)
        
    #print (world.contactCount)
    
  #  for k in world.contacts:
    #    print (k)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()