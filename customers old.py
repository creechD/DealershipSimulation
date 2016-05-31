from stateMachine import *
from Dealership import *

from GameEntity import *
import pygame
from pygame.locals import *

from helpers import *
from random import randint

class newVehicleCustomer(GameEntity):
    """
    This is the class for New Vehicle Customers
    """
    def __init__(self, dealership, image):
        GameEntity.__init__(self, dealership, "Customer", image)
        self.id = 0
        
        self.prefered_sp = None # Tracks with Salesperons the customers likes
        self.engaged_sp = None # Tracks which Salesperson is engaged with the 
                               #  customer
        self.near_by_sp = None # Tracks to see if there are any near by sales 
                               #  people ready
        
        self.actions_per_second = 0.5 # Every 2 seconds actions are done
        self.last_action_time = 0        
        
        self.entered_store = self.dealership.elapsedTime
        self.timeLimit = 10        
        
        self.previous_action = None
        
        self.idle_state = customer_idle(self)
        self.shopping_state = customer_shopping(self)
        self.engaged_state = customer_engaged_with_sp(self)
        self.left_state = customer_left(self)        
        
        self.brain.add_state(self.idle_state)
        self.brain.add_state(self.shopping_state)
        self.brain.add_state(self.engaged_state)
        self.brain.add_state(self.left_state)
        
    def activity_check(self):
        # this function checks to see if the customer can move yet
        return self.dealership.elapsedTime - self.last_action_time > 1/self.actions_per_second        
        
class customer_idle(State):
    def __init__(self, customer):
        State.__init__(self, "idle")
        self.customer = customer
    
    def do_actions(self): # Required
        pass
    
    def check_conditions(self): # Required
        # This checks to see if the customer needs to change what they are
        #  presently doing.
        # idle customers can either start shopping or leave the store
        can_move = self.customer.activity_check()
        if can_move:
            # This means that the customer has not acted within the last 2 seconds
            action_roll = randint(0, 1)
            if action_roll == 1:
                return "shopping"
            elif self.customer.dealership.elapsedTime - self.customer.entered_store > self.customer.timeLimit:
                return "left"
            
    def exit_actions(self): # Required
        self.previous_action = "idle"
    
    def entry_actions(self):  # Required
        print "Customer", self.customer.id, "is now idle"

            
class customer_shopping(State):
    def __init__(self, customer):
        State.__init__(self, "shopping")
        self.customer = customer
    
    def find_near_by_sp(self):
        # This checks to see if there are any salespeople near by ready to help
        near_by_sp = None
        for salesPerson in self.customer.dealership.salesPeople.values():
            if salesPerson.helping_customer != None:
                if salesPerson.helping_customer.id == self.customer.id:
                    # There is a salesperson near by
                    near_by_sp = salesPerson
        # Save result of search
        self.customer.near_by_sp = near_by_sp

    
    def do_actions(self): # Required
        pass
    
    def check_conditions(self): # Required
        # This checks to see if the customer needs to change what they are
        #  presently doing.
        can_move = self.customer.activity_check()
        if can_move:
            # This means that the customer has not acted within the last 2 seconds            
            action_roll = randint(0, 4)
            self.find_near_by_sp() # Find any near by Salespeople
            
            #print self.customer.id, "Customer shopping", action_roll, "near by Salesperson", self.customer.near_by_sp.id
            if action_roll == 0:
                return "idle"
            elif action_roll > 2 and self.customer.near_by_sp != None:
                return "engaged"
            elif action_roll == 2 and self.customer.near_by_sp == self.customer.prefered_sp and self.customer.near_by_sp != None:
                # This is the extra bonus for having the prefered SP around
                return "engaged"
            
    def exit_actions(self): # Required
        self.customer.previous_action = "shopping"
    
    def entry_actions(self): # Required
        print "Customer", self.customer.id, "is now shopping"
  
  
class customer_engaged_with_sp(State):
    def __init__(self, customer):
        State.__init__(self, "engaged")
        self.customer = customer
    
    def do_actions(self): # Required
        pass
    
    def check_conditions(self): # Required
        # This checks to see if the customer needs to change what they are
        #  presently doing.
        can_move = self.customer.activity_check()
        if can_move:
            action_roll = randint(0, 1)
            if action_roll == 1:
                # The salesperson didn't help the customer find what they were 
                #  looking for. 
                self.customer.near_by_sp = None
                self.customer.engaged_sp = None
                return "shopping"
            
    def exit_actions(self): # Required
        self.previous_action = "engaged"
    
    def entry_actions(self): # Required
        self.customer.engaged_sp = self.customer.near_by_sp
        print "Customer", self.customer.id, "is now engaged with salesperson", self.customer.engaged_sp.id
   
   
class customer_left(State):
    # Customer left the store.  They stay in the dealer's CRM and in the future
    #  can return (Not yet implemented)
    def __init__(self, customer):
        State.__init__(self, "left")
        self.customer = customer
    
    def do_actions(self): # Required
        pass
    
    def check_conditions(self): # Required
        pass
            
    def exit_actions(self): # Required
        pass
    
    def entry_actions(self): # Required
        print "Customer", self.customer.id, "has left the dealership"
        self.customer.dealership.remove_customer(self.customer)    
    