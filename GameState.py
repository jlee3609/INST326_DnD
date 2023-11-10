from argparse import ArgumentParser
import json
import random

class GameState:
    """
    
    Attributes:
        items ():
        locations ():
        party (dict of Players, player name is key): all Players in a party.
    """
    def __init__(self, items, locations, party):
        """
        """
        self.items = items
        self.locations = locations
        self.party = party
        self.curr_location = "Village Square"
            
    def new_turn(self):
        """
        """
        print(f"You are currently in {self.curr_location}")
        
        # prob needs to be command line arg but like \(i.i)/???
        action = input("What would you like to do? ")
        if action == "travel":
            destination = input(f"Where would you like to go? {self.locations['children']}")
            self.travel(destination)
            
    def shop(self):
        """
        """
        shoplist = []
        for _ in range(3):
            #if you'll still have items left, leave it in the dict for now
            #otherwise, pop it for now, but if it isn't bought we'll put it back.
            item =random.choice(self.items)
            if self.items[item]-1 != 0:
                self.items[item] = self.items[item]-1
                shoplist.append(item)
            else:
                shoplist.append(item)
                self.items.pop[item]
        for item in shoplist:
            item.stats()
        answer = input("Would you like to purchase an item? (y/n)")
        if answer == "y":
            purchase = input("Please input the index of the item you desire: (1,2,3)")
            victim = input("Please input the name of who is purchasing the item:")
            confirmation = input(f"{victim} will lose {item.cost} and gain a(n) \
                {item.name}. Confirm purchase? (y/n)")
            if confirmation == "y":
                self.party[victim].bag.append(item)
                self.party[victim].money -= item.cost
                shoplist.pop()
                print("Thank you for your purchase.")
            else:
                print("Purchase cancelled. The merchant side-eyes you and \
                    reshuffles her wares. You sense she won't sell you anything more.")
                for item in shoplist:
                    
        else:
            print("The merchant side-eyes you and reshuffles her wares. \
                She leaves as quietly as she came.")
                
    def encounter(self):
        """
        """
        pass
    def battle(self):
        """
        """
        pass
    def travel(self, destination):
        """
        """
        self.curr_location = destination
        self.scenario()
        
    def scenario(self):
        """
        """
        x = random.randint(1,3)
        
        if x == 1:
            self.shop()
        elif x == 2:
            self.battle()
        else:
            self.encounter()
          
    