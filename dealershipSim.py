# -*- coding: utf-8 -*-
"""
Created on Sat May 28 12:20:14 2016

@author: DavidCreech
"""
import pygame

pygame.init()
        
from dealership import *
from datetime import datetime

black = (  0,   0,   0)
white = (255, 255, 255)
blue =  (  0,   0, 255)
green = (  0, 255,   0)
red =   (255,   0,   0)

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class dealershipSim:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=1024,height=512):
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
        
        self.paused = False
        
    def printInfo(self, label, value, xlocation, ylocation, debug = False):
         """
         Prints information about what is currently going on in the dealership 
         """               
         self.screen.blit(self.background, (0, 0))     
         if pygame.font:
            font = pygame.font.Font(None, 20)
            text = font.render(label + " %s" % value
                                , 1, (255, 0, 0))
            textpos = text.get_rect(left = xlocation, bottom = ylocation)
            self.screen.blit(text, textpos)
            pygame.display.update(textpos)
            if debug:
                print label, value, xlocation, ylocation    
                
    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
        
    def button(self, msg,x,y,w,h,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #print(click)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, blue,(x,y,w,h))
    
            if click[0] == 1 and action != None:
                action()         
        else:
            pygame.draw.rect(self.screen, green, (x,y,w,h))
    
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)            

    def pause(self):
        if self.paused == True:
            self.paused = False
        else:
            self.paused = True

    def MainLoop(self):
        """This is the Main Loop of the Game"""
        dlr = dealership()
        
        
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
            if (self.paused == False):
                pauseText = "Pause Game"
            else:
                pauseText = "Unpause Game"
                
            self.button(pauseText, 0, 0, 200, 100, self.pause)            
            # Keep track of how much time has elapsed for timer purposes
            #self.elapsedTime += self.waitTime * 0.001
            dlr.clock.tick(20)
            dlr.elapsedTime += 1.0/20

            """ 
            Here is the main loop where all actions will take place
            I want events to happen every 1 second
            """
            #pygame.time.delay(self.waitTime)
          
            if self.paused == False:            
                # Run Game Actions
                dlr.customerActions(dlr.elapsedTime)
                
                # Update Display         
                pygame.display.flip()
                self.printInfo("Elapsed Time", int(dlr.elapsedTime), 0, self.height);
                self.printInfo("Customers in Store", len(dlr.customers), 0, self.height - 20);
                self.printInfo("Customers idling", dlr.idle, 0, self.height - 40);
                self.printInfo("Customers shopping", dlr.shopping, 0, self.height - 60);
                
                #pygame.display.flip()
            else:
                self.printInfo("The simulation is", "paused", 0, self.height-80);
            dlr.clock.tick(60)
            
        pygame.quit()    
        

if __name__ == "__main__":
    MainWindow = dealershipSim()
    MainWindow.MainLoop()   