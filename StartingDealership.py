#! /usr/bin/env python

import levelBase
from helpers import load_image



class level(levelBase.Level):
    """Starting Dealership"""
    
    def __init__(self):
        self.BLOCK = 1
        self.SNAKE = 2
        self.PELLET = 0
    
    def getLayout(self):
        return [[9, 9, 9 ,9, 9, 9, 9, 9],\
                [9, 9, 9, 9, 9, 9, 9, 9],\
                [9, 1, 1, 1, 1, 1, 1, 9],\
                [9, 0, 0, 0, 0, 0, 0, 9],\
                [9, 0, 1, 1, 0, 1, 1, 9],\
                [9, 0, 2, 0, 0, 0, 0, 9],\
                [9, 0, 1, 1, 0, 1, 0, 9],\
                [9, 0, 0, 0, 0, 1, 0, 9]
             
                
        
    def getSprites(self):
        block, rect = load_image('')
        pellet, rect = load_image('pellet.png',-1)
        snake, rect = load_image('snake.png',-1)
        return [pellet,block,snake]
        