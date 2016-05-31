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

pygame.transform.rotate(Surface, angle)
"""


import os, sys
import pygame
import time
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=512):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
        self.startTime = pygame.time.Clock()
        self.elapsedTime = 0
        self.waitTime = 1000
        
        self.customers

    def printInfo(self, label, value, xlocation, ylocation, debug = False):
        """
        Prints information about what is currently going on in the dealership 
        """               
        self.screen.blit(self.background, (0, 0))     
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render(label + " %s" % value
                                , 1, (255, 0, 0))
            textpos = text.get_rect(left = xlocation, top = ylocation)
            self.screen.blit(text, textpos)
            pygame.display.update(textpos)
            if debug:
                print label, value, xlocation, ylocation
        
    def customerActions(self):
        pass
                                                 
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        running = True
        while running:

            """ Section for handleing exiting the game """
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print "Exiting game..."
                        running = False
                        break
                if event.type == pygame.QUIT:
                    print "Quiting"
                    running = False
                    break
                        
            # Keep track of how much time has elapsed for timer purposes
            self.elapsedTime += self.waitTime * 0.001
            
            
            """ 
            Here is the main loop where all actions will take place
            I want events to happen every 1 second
            """
            pygame.time.delay(self.waitTime)
          
            if 1 == 1:            
                # Run Game Actions
                self.customerActions()
                
                # Update Display                
                self.printInfo("Elapsed Time", self.elapsedTime, 0, 0);
                self.printInfo("Customers in Store", 0, 0, 40, debug = True);
                
                pygame.display.flip()

                    
            
        pygame.quit()
        

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()         

                                     

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                