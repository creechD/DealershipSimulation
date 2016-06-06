
from stateMachine import *
from Dealership import *

from GameEntity import *
import pygame
from pygame.locals import *

from helpers import *
from random import randint

class newVehicleSalesPerson(GameEntity):
    """
    This is the class for New Vehicle Customers
    """
    def __init__(self, dealership, image):
        GameEntity.__init__(self, dealership, "SalesPerson", image)
        self.id = 0
        self.startTime = 0 # To keep track of how long the sales person has 
                           #  been working        

        self.actions_per_second = 1 # Every 1 seconds actions are done
        self.last_action_time = 0           
        
        self.helping_customer = None # Tracks which customer the Salesperson is
                                     #  currently helping
        self.idle_state = salesPerson_idle(self)
        self.near_by_state = salesPerson_near_by(self)
        self.helping_state = salesPerson_helping(self)
        
        self.brain.add_state(self.idle_state)
        self.brain.add_state(self.near_by_state)
        self.brain.add_state(self.helping_state)
        
    def find_customer(self):
        # This finds out if there are any customers in need of help         
        customer_to_help = None
        
        for customer in self.dealership.customers.values():
            if customer.brain.active_state.name in ("shopping", "idle") and customer.near_by_sp == None:
                customer_to_help = customer                           
        # If no customers are found to help, this sets helping_customer to None                
        self.helping_customer = customer_to_help    
        
    def activity_check(self):
        # this function checks to see if the customer can move yet
        return self.dealership.elapsedTime - self.last_action_time > 1/self.actions_per_second         
       
class salesPerson_idle(State):
    # idle sales people are ready to help customers
    def __init__(self, salesPerson):
        State.__init__(self, "idle")
        self.salesPerson = salesPerson
              
    def check_conditions(self): # Required
        # Check to see if there are any customers in need of help     
        can_move = self.salesPerson.activity_check()
        if can_move:
            self.salesPerson.find_customer()
            if self.salesPerson.helping_customer != None:
                return "near_by"
        
    def exit_actions(self): # Required
        pass
    
    def entry_actions(self):  # Required
        self.salesPerson.helping_customer = None
        print "Salesperson", self.salesPerson.id, "is now idle"
    
    def do_actions(self): # Required
        pass
    
class salesPerson_near_by(State):
    # idle sales people are ready to help customers
    def __init__(self, salesPerson):
        State.__init__(self, "near_by")
        self.salesPerson = salesPerson
                                       
    def check_conditions(self): # Required
        can_move = self.salesPerson.activity_check()
        if can_move:
            # Check to see if the customer has engaged with the salesperson
        
            # Note: this shouldn't throw an error because in order to get into 
            #  this state, the salesperson needed to by helping a customer
            helping_customer = self.salesPerson.helping_customer 
            customer_brain_state = helping_customer.brain.active_state.name
            customer_engaged_sp = helping_customer.engaged_sp
            if customer_brain_state == "engaged":
                if customer_engaged_sp.id == self.salesPerson.id:
                    return "helping"
                else:
                    # This means that the customer is engaged with a different
                    #  salesperson
                    return "idle"
            else:
                # This means that the customer didn't engaged with the sp
                #TODO: Add logic here to find a different customer
                return "idle"
    
    def exit_actions(self): # Required
        pass
    
    def entry_actions(self):  # Required
        print "Salesperson", self.salesPerson.id, "walks up to customer", self.salesPerson.helping_customer.id
    
    def do_actions(self): # Required
        pass    
    
    
class salesPerson_helping(State):
    # idle sales people are ready to help customers
    def __init__(self, salesPerson):
        State.__init__(self, "helping")
        self.salesPerson = salesPerson

    def check_conditions(self): # Required
        can_move = self.salesPerson.activity_check()
        if can_move:
            # Check to see if the customer has engaged with the salesperson
        
            # Note: this shouldn't throw an error because in order to get into 
            #  this state, the salesperson needed to by helping a customer
            helping_customer = self.salesPerson.helping_customer 
            customer_brain_state = helping_customer.brain.active_state.name
            if customer_brain_state in ("shopping", "idle"):
                # This means that the customer disengaged from the salesperson 
                #TODO: Add logic here to find a different customer
                return "idle"
    
    def exit_actions(self): # Required
        pass
    
    def entry_actions(self):  # Required
        print "Salesperson", self.salesPerson.id, "starts helping customer", self.salesPerson.helping_customer.id
    
    def do_actions(self): # Required
        pass    
    