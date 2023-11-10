from argparse import ArgumentParser
import Player
import json
import random

def generate_npc(gamestate):
    names = ["Aeliana", "Thoren", "Elowen", "Kael", "Seraphim", "Lirael", "Garrick", 
            "Isabeau", "Eldon", "Lyria", "Caden", "Rowena", "Thaddeus", "Anara",
            "Finnian", "Livia", "Dorian", "Tamsin", "Galadriel", "Merek"]
    classes = ["Mage", "Healer", "Tank", "Assassin", "Berserker"]
    npc = Player.Player(random.choice(names), random.choice(classes))
    npc.buy(random.choice(item for item in gamestate.items if item.cost <=100))
class GameState:
    """
    
    Attributes:
        items (dict of items, quantity is value): 
        locations ():
        travel_options ():
        location_data ():
        party (dict of Players, player name is key): all Players in a party.
        curr_location ():
        parent_location ():
    """
    def __init__(self, items, location_data, party):
        """
        """
        self.items = items
        self.locations = {}
        self.travel_options = {}
        self.curr_location = "Village Square"
        for place in location_data["locations"]:
            self.locations.append(place)
        self.party = party
        for place in location_data["children"][self.curr_location]:
            self.travel_options.append(place)     
            
    def new_turn(self):
        """
        """
        print(f"You are currently in {self.curr_location}")
        
        # prob needs to be command line arg but like \(i.i)/???
        action = input("What would you like to do? ")
        if action == "travel":
            destination = input(f"Where would you like to go?:"
                                f"{self.travel_options}")
            self.travel(destination)
            
    def shop(self):
        """Opens up a shop that one item can be purchased from
        
        Side effects:
            Potentially removes 1 item from items dictionary
            Potentially adds 1 item to 1 player's bag
            Potentially removes gold from 1 player's money
            Prints to terminal
        
        """
        shoplist = []
        print("A merchant beckons you from a nearby alley. \
            She opens a dark box, revealing the treasures within.")
        for _ in range(3):
            #if you'll still have items left, leave it in the dict for now
            #otherwise, pop it for now, but if it isn't bought we'll put it back.
            item =random.choice(self.items)
            if self.items[item]-1 != 0:
                self.items[item] -= 1
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
            if victim not in self.party:
                victim = input("Please input a valid name:")
            confirmation = input(f"{victim} will lose {item.cost} and gain a(n) \
                {item.name}. Confirm purchase? (y/n)")
            if confirmation == "y":
                #add item to player bag, subtract money, remove item from shop
                self.party[victim].buy(item)
                shoplist.remove(item)
                print("Thank you for your purchase.")
                #put unsold items back
                for item in shoplist:
                    if item in self.items:
                        self.items[item] +=1
                    else:
                        self.items[item] = 1
            else:
                print("Purchase cancelled. The merchant side-eyes you and \
                    reshuffles her wares. You sense she won't sell you anything more.")
                for item in shoplist:
                    if item in self.items:
                        self.items[item] +=1
                    else:
                        self.items[item] = 1
        else:
            print("The merchant side-eyes you and reshuffles her wares. \
                She leaves as quietly as she came.")
                
    def encounter(self):
        """An encounter with a randomly generated npc
        """
        npc = generate_npc(self)
        print("You encounter {npc.name}! They are a {npc.class} in possession of a ")
        attitude = random.randrange(20)
        if attitude in range(7):
            #hostile lollll
            #can choose to run or battle
            #if they choose to run, do a speed check
            #if they're too slow then they're losers and get ambushed
            #call the battle function
            pass
        elif attitude < 14:
            #ambivalent
            pass
        else:
            #generous
            #give money, give item, restore hp if class is healer
            pass
    def battle(self, status):
        """
        """
        #status can be ambush (bad for player), surprise (good for player), or neutral
        pass
    def travel(self, destination):
        """
        """
        self.parent_location = self.curr_location
        self.travel_options.append(self.parent_location)
        self.curr_location = destination
        self.scenario()
        
    def scenario(self):
        """
        """
        options = self.locations["children"][self.curr_location]
        x = random.choice(options)
        if x == "s":
            self.shop()
        elif x == "b":
            self.battle()
        else:
            self.encounter()
          
    