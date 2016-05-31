# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:06:11 2016

@author: DavidCreech
"""
from Dealership import *
from stateMachine import *

import pygame
from pygame.locals import *

class GameEntity(object):
    def __init__(self, dealership, name, image):
        self.dealership = dealership
        self.name = name
        
        self.image = image
        self.orientation = 0

        self.brain = StateMachine()

        self.id = 0
        
        self.tp = 0

    def render(self, surface):
        pass

    def process(self, time_passed):
        self.brain.think()
        self.tp = time_passed