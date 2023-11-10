from argparse import ArgumentParser
import json

class GameState:
    def __init__(self, items, locations, party):
        self.items = items
        self.locations = locations
        self.party = party
        self.curr_location = "Village Square"
            
    def new_turn(self):
        print(f"You are currently in {self.curr_location}")
        
        # needs to be command line arg but like \(i.i)/
        action = input("What would you like to do? ")
        if action == "travel":
            destination = input(f"Where would you like to go? {self.locations['children']}")
            self.travel(destination)
            
    def shop(self):
        pass
    def encounter(self):
        pass
    def travel(self, destination):
        self.curr_location = destination
        self.scenario()
        
    def scenario(self):
        pass  
    