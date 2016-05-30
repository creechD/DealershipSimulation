# -*- coding: utf-8 -*-
"""
Game Board

Each block is 16x16 pixels

Images to create
Store floor
0
Store wall
1 - Top
2 - Right (rotate 90)
3 - Bottom (Rotate 180)
4 - Left (Rotate 270)

Stone wall corner
5 - Top Right
6 - Bottom Right (Rotate 90)
7 - Bottom Left (Rotate 180)
8 - Top Left (Rotate 270)
Parking lot
Store wall with door
Desk


"""


import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=512,height=512):
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
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(500, 30)
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        self.snake.move(event.key)
                        
            """Check for collision"""
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
        """Load the sprites that we need"""
        
        """figure out how many pellets we can display"""
        nNumHorizontal = int(self.width/64)
        nNumVertical = int(self.height/64)       
        """Create the Pellet group"""
        self.pellet_sprites = pygame.sprite.Group()
        """Create all of the pellets and add them to the 
        pellet_sprites group"""
        for x in range(nNumHorizontal):
            for y in range(nNumVertical):
                self.pellet_sprites.add(Pellet(pygame.Rect(x*64, y*64, 64, 64)))        
        
        
class Pellet(pygame.sprite.Sprite):
        
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('Corner.gif', 'Walls', -1)
        if rect != None:
            self.rect = rect
        

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()         

                                     

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                