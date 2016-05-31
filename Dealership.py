# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:59:14 2016

@author: DavidCreech
"""
import os, sys
import pygame

from pygame.locals import *
from helpers import *
from Customers import *
from SalesPerson import *

from random import randint

class Dealership(object): # Class that stores basically EVERYTHING!

    def __init__(self):


        self.clock = pygame.time.Clock()
        self.elapsedTime = 0.0
        self.waitTime = 2.0
        
        # Each customer is given a unique ID so that the program can find it
        self.customers = {}
        self.customer_id = 0
        
        # Customers that have left the dealership
        self.left_customers = {}
        self.left_customer_id = 0

        self.idle = 0
        self.shopping = 0
        self.engaged = 0
        

        # Each sales person is given a unique ID so that the program can find it
        self.salesPeople = {}
        self.salesPerson_id = 0
        
        
        self.last_customer_time = 0
        
        self.new_game()
        # 
        
    def new_game(self):
        # Each customer is given a unique ID so that the program can find it
        self.customers = {}
        self.customer_id = 0
        
        # Customers that have left the dealership
        self.left_customers = {}

        # Each sales person is given a unique ID so that the program can find it
        self.salesPeople = {}
        self.salesPerson_id = 0
        
        self.start_game()
    
    def start_game(self):
        # Start game
        # Start by generating all of the Salespeople and customers
        salesPeople_count = 1
        customer_count = 1

        for salesPeople_no in xrange(salesPeople_count):
            new_sp = newVehicleSalesPerson(self, "image")
            new_sp.brain.set_state("idle")
            self.add_salesPerson(new_sp)
       
        for customer_no in xrange(customer_count):
            new_customer = newVehicleCustomer(self, "image")
            new_customer.brain.set_state("shopping")
            self.add_customer(new_customer)
   
    def add_customer(self, customer): # Used to add customers
        self.customers[self.customer_id] = customer
        customer.id = self.customer_id
        print "Customer", customer.id, "walked into the dealership"
        self.customer_id += 1
       
    def remove_customer(self, customer): #function for removing customers
        self.left_customers[self.left_customer_id] = customer
        self.left_customer_id += 1
        del self.customers[customer.id]
  
    def add_salesPerson(self, salesPerson): # Used to add customers 
        self.salesPeople[self.salesPerson_id] = salesPerson
        salesPerson.id = self.salesPerson_id
        self.salesPerson_id += 1
       
    def remove_salesPerson(self, salesPerson): #function for removing customers
        del self.salesPeople[salesPerson.id]     
        
    def customerActions(self, time_passed):
        # Check to see if a new customer walks in

        if time_passed - self.last_customer_time < self.waitTime:
            pass
        else:
            self.last_customer_time = time_passed
            
            new_customer_chance = randint(0, 9)
            #print "Trying to add new customer.  Rolled a", new_customer_chance
            if new_customer_chance > 7:
                new_customer = newVehicleCustomer(self, "image")
                new_customer.brain.set_state("shopping")
                self.add_customer(new_customer)
            self.process(time_passed)
            
    def count_States(self):
        self.idle = 0
        self.shopping = 0
        
        for customer in self.customers.values():
            if customer.brain.active_state.name == "idle":
                self.idle += 1
            elif customer.brain.active_state.name == "shopping":
                self.shopping += 1
            elif customer.brain.active_state.name == "engaged":
                self.engaged += 1
            else:
                print "Customer brain state not counted", customer.brain.active_state.name
                
    def process(self, time_passed):
        for customer in self.customers.values():
            customer.process(time_passed)
            
        for salesPerson in self.salesPeople.values():
            salesPerson.process(time_passed)
        self.count_States()
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       