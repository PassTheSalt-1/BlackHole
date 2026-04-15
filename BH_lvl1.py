import pygame ## for graphics, animations, and handling input. useful for displays and drawing functions.
import random
import math
import numpy as np



##Setup 

WIDTH, HEIGHT = 1000, 800 ## screen dimensions
CENTER = np.array([WIDTH / 2, HEIGHT /2]) ## initialize blackhole center position

pygame.init() ## start the pygame engine
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #create the windows
clock = pygame.time.Clock()

fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) ## Transparency overlay settings
fade.fill((0,0,0,25))

## Initialize Black hole properties 
BH_MASS = 5000
G = 0.05
EVENT_HORIZON = 25

#Create particlae class, using random to spawn particles at random times, color, and position.
class Particle:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi) ## randome particles spawning logic, both direction and distance
        radius = random.uniform(150,350)

        self.pos = CENTER + np.array([  ## np function creates a vector, and places particles around center
            math.cos(angle) * radius,   ## convert angles into circular coordinates
            math.sin(angle) * radius
        ])

        tangent = np.array([ ## creates perpendicular directions simulating orbit
            -math.sin(angle),
            math.cos(angle)
        ])

        speed = math.sqrt(G* BH_MASS / radius) * 1.2 ## orbital velocity
        self.vel = tangent * speed

        self.color = (255, random.randint(100,225), 0)
    def update(self):

        direction = CENTER - self.pos
        distance = np.linalg.norm(direction) ## computes the vector length.

        if distance < EVENT_HORIZON: # if particle too close to event horizon destroy it!
            return False
        
        direction = direction / distance

        accel = direction * (G * BH_MASS / distance ** 2) ## Simulating gravity

        self.vel += accel ## Euler integration velocity changes by acceleration
        self.pos += self.vel ## position changes by velocity.

        return True
    def draw(self): ## draw the particles 
        pygame.draw.circle(
            screen,
            self.color,
            self.pos.astype(int),
            3
        )
##Create particles 
particles = [Particle() for _ in range (300)]

##Main Loop

running = True
while running:

    ##Apply the transparent fade
    screen.blit(fade, (0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    
    
    pygame.draw.circle(screen, (50,20,20),CENTER.astype(int),EVENT_HORIZON+8) ## draw red horizon ring 
    pygame.draw.circle(screen, (0,0,0), CENTER.astype(int),EVENT_HORIZON) ## draw black hole

    new_particles = []

    for p in particles:
        alive = p.update()
        if alive:
            p.draw()
            new_particles.append(p)

    particles = new_particles

    pygame.display.flip()## refresh the screen after drawing.
    clock.tick(60) ## controls the FPS of the simulation

pygame.quit()