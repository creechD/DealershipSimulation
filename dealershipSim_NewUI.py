#!/usr/bin/env python
from __future__ import division

#Interphase - Copyright (C) 2009 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>
#
#"""
#Interphase Demo
#
#Interphase Module
#Project Site: http://gatc.ca/
#"""

import interphase
import pygame
import random

from Dealership import *

__docformat__ = 'restructuredtext'


module_info = """Interphase Module\n\nThe module adds interface panel functionality to a Pygame application. It was developed as a simple GUI with the goal to simulate a digital display panel. The module provides interface and control objects to design a panel, and numerous methods to manage the panel from the application code."""


class dealershipSim_NewUI(interphase.Interface):
    """
    Interphase interface.
    """

    def __init__(self):
        self.pygame_initiate()
        interphase.Interface.__init__(self, position=(250,450), color=(43,50,58), size=(400,400), moveable=False, position_offset=(0,95), control_minsize=(25,25), control_size='auto', font_color=(175,180,185), tips_fontcolor=(175,180,185), scroll_button='both')
        self.dealership_initiate()
        self.update_rect = []
        infoboxText = "Initialized"

    def add_controls(self):
        """Add interface controls."""
        Control_list = ['Intro Textbox', 'Control 1', 'Control 2', 'Layout', 'Puzzle', 'Doc', 'Exit']
        Control_tip = ['Interphase Intro', 'Control Panel 1', 'Control Panel 2', 'Control Placement', 'Sliding Control', 'Click to Exit']
        Control_link = [ ['Interphase'], ['Select1'], ['Setting1', 'Setting2', 'Files'], ['Moveable'],['Puzzle'], ['Doc'] , ['Interphase_url']]
        self.add(
            identity = 'PauseGame',
            control_type = 'function_toggle',
            position = (32,17),
            size = (60,30),
            control_list = ['Pause', 'Resume'],
            link = [ [], [] ])
        self.add(
            identity = 'ShowCustomerAttributes',
            control_type = 'function_toggle',
            position = (32,60),
            size = (60,45),
            control_list = ['Show Customer Attributes', 'Hide Customer Attributes'],
            link = [ [], ['InfoBox', 'agent_type_select','agent_select'] ])
        self.add(
            identity = 'InfoBox',
            control_type = 'textbox',
            position = (275,62),
            size = (219,64),
            color = (49,57,65),
            font_color = (125,175,200),
            font_size = 12,
            font_type = 'arial',
            control_list = [],
            text_paste = True,
            label_display = False)
        # Combo box to select the agent to investigate
        self.add(
            identity = 'agent_type_select',
            control_type = 'function_select',
            position = (125,25),
            size = (75, 30),
            control_list = ['Customer', 'Salesperson'])
        self.add(
            identity = 'agent_select',
            control_type = 'function_select',
            position = (125,60),
            size = (75, 30),
            control_list = ['0'])
        #self.doc_interface = DealershipInfo(self.screen)

    def pygame_initiate(self):
        """Initiate pygame."""
        pygame.display.init()   #pygame.init()
        pygame.display.set_caption('Dealership Simulation')
        self.screen = pygame.display.set_mode((500,500))
        self.background = pygame.Surface((500,500))
        self.clock = pygame.time.Clock()
        pygame.display.flip()

    def dealership_initiate(self):
        """Initiate dealership."""
        self.elapsedTime = 0
        self.waitTime = 1000
        self.paused = False

    def pygame_check(self):
        """Check user input."""
        terminate = False
        for event in pygame.event.get():
            if event.type == interphase.EVENT['controlselect']:
                if event.state.control == 'Control' and event.state.button == 'Control':
                    if event.state.value == 'Exit':
                        terminate = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate = True
            elif event.type == pygame.QUIT:
                terminate = True
        self.clock.tick(40)
        return terminate

    def pause(self):
        if self.paused == True:
            self.paused = False
        else:
            self.paused = True

    def updateCustomerAttributes(self, dlr, state):
        customerList = dlr.customers
        customerListString = ' '.join(map(str, customerList)) # Converts list to string
        print customerListString
        debugOutput = state.controls['agent_type_select'].get_value()
        state.controls['InfoBox'].set_value(debugOutput)

    def showCustomerAttributes(self, dlr, state):
        customer_id = state.controls['agent_select'].get_value()
        customer = dlr.get_customer(customer_id)
        if customer != None:
                
            dlr_customer_id = customer.id
            output_text = "Selected customer ID:" + str(customer_id)
            output_text +=  "\nFound customer ID:" +  str(dlr_customer_id)           
            
            #output_text += "\nhelping_customer" + customer.helping_customer

            state.controls['InfoBox'].set_value(output_text)
        else:
            state.controls['InfoBox'].set_value("Invalid customer ID")
        
    
    def showSalespersonAttributes(self, dlr, state):
        state.controls['InfoBox'].set_value("Salesperson Attributes")
    

    def updateAgentList(self, dlr, state):
        if state.controls['agent_type_select'].get_value() == "Customer":
            agentList = []
            for customer in dlr.customers.values():
                agentList.append(customer.id)
            #agentList = range(0, len(dlr.customers))
            state.controls['agent_select'].set_list(agentList)
            self.showCustomerAttributes(dlr, state)
        elif state.controls['agent_type_select'].get_value() == "Salesperson":
            agentList = range(0, len(dlr.salesPeople))
            state.controls['agent_select'].set_list(agentList)
            self.showSalespersonAttributes(dlr, state)
    
    def update(self, dlr):
        """
        Interface update returns state object.

        State Object
            panel:              Interface panel
            controls:           Interface controls
            panel_active        Panel active
            panel_update        Panel update
            panel_interact:     Pointer interface interact
            control_interact:   Pointer control interact
            button_interact:    Pointer button interact
            control:            Control selected
            button:             Button selected
            value:              Control value
            values:             Panel control values
        """
        dlr.clock.tick(20)
        state = interphase.Interface.update(self)
        if state.control:
            print "state.control", state.control
            if state.control == "PauseGame":
                self.pause()
            #elif state.control == "ShowCustomerAttributes":
            #    self.updateCustomerAttributes(dlr, state)
            elif state.control in ("agent_type_select", "agent_select"):
                self.updateAgentList(dlr, state)
            
        if self.pygame_check():
            self.deactivate()
        if self.paused == False:
            dlr.elapsedTime += 1.0/20
            #self.get_control("InfoBox").set_
            dlr.dealershipActions(dlr.elapsedTime)
        return state
        
def run():
    panel = dealershipSim_NewUI()
    dlr = Dealership()
    
    run_demo = True
    while run_demo:
        panel.update(dlr)
        if panel.is_active():
            if panel.is_update():
                panel.clear(panel.screen,panel.background)
                panel.update_rect.extend( panel.draw(panel.screen) )
            if panel.update_rect:
                pygame.display.update(panel.update_rect)
                panel.update_rect = []
        else:
            run_demo = False
    pygame.quit()   

def main():
    run()

if __name__ == '__main__':
    main()

