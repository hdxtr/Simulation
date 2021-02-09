import pygame
import pymunk
import pymunk.pygame_util
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import json

pygame.init()
screen = pygame.display.set_mode((1200,600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0.0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

def loadConfig(configFile):

    with open(f'configFile.json', 'r') as cfg:
        config = cfg.read()

    return json.loads(config)

class Swing():

    def __init__(self):
        self.objects = self.generateSwing()

    def generateSwing(self):
        rod = pymunk.Body(10, 10)
        rod.position = (300, 100)
        rod.mass = 1
        rod.friction = 0
        rod_shape = pymunk.Segment(rod, (0,0), (100,200), 5)

        top = pymunk.Body(10,10, pymunk.Body.STATIC)
        top.position = (300, 150)
        top_shape = pymunk.Poly.create_box(top, (20,20))

        pivot = pymunk.PivotJoint(top, rod, (300, 150))
        pivot.collide_bodies = False

        return {'rod' : [rod, rod_shape], 'top' : [top, top_shape], 'pivot' : pivot}

    def render(self, screen):
        pass

    def update(self):
        self.eventListener()

    def eventListener(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.kick(1)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.kick(-1)


class LearningArea():

    def __init__(self, configFile):
        pass

swing = Swing()

space.add(*swing.objects['rod'], *swing.objects['top'], swing.objects['pivot'])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    space.step(1/60)
    screen.fill((255,255,255))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
