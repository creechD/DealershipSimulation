#! /usr/bin/env python

import os, sys
import pygame
import level001
import basicSprite
from pygame.locals import *
from helpers import *
from snakeSprite import Snake

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

BLOCK_SIZE = 24

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
                                                          
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        """Load All of our Sprites"""
        self.LoadSprites();
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        """Draw the blocks onto the background, since they only need to be 
        drawn once"""
        self.block_sprites.draw(self.background)
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.snake.MoveKeyDown(event.key)
                elif event.type == KEYUP:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.snake.MoveKeyUp(event.key)
            """Update the snake sprite"""        
            self.snake_sprites.update(self.block_sprites)
                        
            """Check for a snake collision/pellet collision"""
            lstCols = pygame.sprite.spritecollide(self.snake
                                                 , self.pellet_sprites
                                                 , True)
            """Update the amount of pellets eaten"""
            self.snake.pellets = self.snake.pellets + len(lstCols)
                        
            """Do the Drawging"""               
            self.screen.blit(self.background, (0, 0))     
            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Pellets %s" % self.snake.pellets
                                    , 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.background.get_width()/2)
                self.screen.blit(text, textpos)
               
            self.pellet_sprites.draw(self.screen)
            self.snake_sprites.draw(self.screen)
            
            pygame.display.flip()
                    
    def LoadSprites(self):
        """Load all of the sprites that we need"""
        """calculate the center point offset"""
        x_offset = (BLOCK_SIZE/2)
        y_offset = (BLOCK_SIZE/2)
        """Load the level"""        
        level1 = level001.level()
        layout = level1.getLayout()
        img_list = level1.getSprites()
        
        """Create the Pellet group"""
        self.pellet_sprites = pygame.sprite.Group()
        """Create the block group"""
        self.block_sprites = pygame.sprite.Group()
        
        for y in xrange(len(layout)):
            for x in xrange(len(layout[y])):
                """Get the center point for the rects"""
                centerPoint = [(x*BLOCK_SIZE)+x_offset,(y*BLOCK_SIZE+y_offset)]
                if layout[y][x]==level1.BLOCK:
                    block = basicSprite.Sprite(centerPoint, img_list[level1.BLOCK])
                    self.block_sprites.add(block)
                elif layout[y][x]==level1.SNAKE:
                    self.snake = Snake(centerPoint,img_list[level1.SNAKE])
                elif layout[y][x]==level1.PELLET:
                    pellet = basicSprite.Sprite(centerPoint, img_list[level1.PELLET])
                    self.pellet_sprites.add(pellet)  
        """Create the Snake group"""            
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))                                  

if __name__ == "__main__":
    MainWindow = PyManMain(500,575)
    MainWindow.MainLoop()
       