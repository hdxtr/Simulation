import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import json

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0.0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

def loadConfig(configFile):

    with open(f'{configFile}', 'r') as cfg:
        config = cfg.read()

    return json.loads(config)

class Person():

    def __init__(self):
        pass

    def generatePerson(self):
        torso = pymunk.Body(10, 10)

class Swing():

    def __init__(self, space, swingConfig):
        self.space = space
        self.objects = self.generateSwing(swingConfig)

    def generateSwing(self, config):
        # specifies the top of the swing as defined by topPosition
        top = pymunk.Body(10,1000000, pymunk.Body.STATIC)
        top.position = Vec2d(*config['topPosition'])
        top_shape = pymunk.Poly.create_box(top, (20,20))

        self.space.add(top, top_shape)

        joints = []
        joint_shapes = []
        pivots = []
        for i in config['jointLocations']:
            '''
            Iterate through the list of coordinates as specified by jointLocations,
            relative to the top of the swing
            '''
            point = pymunk.Body(10, 100)
            point.position = top.position + Vec2d(*i)
            point_shape = pymunk.Segment(point, (0,0), (0,0), 5)
            # if the first joint, join to the top, otherwise join to the preceding
            # joint
            if len(joints) == 0:
                pivot = pymunk.PinJoint(top, point, (0,0))
            else:
                pivot = pymunk.PinJoint(joints[-1], point)
            pivot.collide_bodies = False
            joints.append(point)
            joint_shapes.append(point_shape)
            pivots.append(pivot)

            self.space.add(point, point_shape)
            self.space.add(pivot)

        return {'rod' : [joints, joint_shapes], 'top' : [top, top_shape], 'pivots' : pivots}

    def render(self, screen):
        pass

    def update(self):
        self.eventListener()

    def eventListener(self):
        pass


class LearningArea():

    def __init__(self, configFile):
        pass

config = loadConfig('config.json')

swing = Swing(space, config['swingConfig'])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    space.step(1/60)
    screen.fill((255,255,255))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
