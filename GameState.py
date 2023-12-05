from argparse import ArgumentParser
import Player
import json
import random

def generate_npc(gamestate, boss=False):
    """
    """
    names = ["Aeliana", "Thoren", "Elowen", "Kael", "Seraphim", "Lirael", "Garrick", 
            "Isabeau", "Eldon", "Lyria", "Caden", "Rowena", "Thaddeus", "Anara",
            "Finnian", "Livia", "Dorian", "Tamsin", "Galadriel", "Merek"]
    classes = ["Mage", "Healer", "Tank", "Assassin", "Berserker"]
    if boss == False:
        npc = Player.Player(random.choice(names), random.choice(classes), "NPC", 20)
        npc.buy(random.choice(item for item in gamestate.items if item.cost <=100))
    else:
        boss_names = ["Nicole", "Ariel", "Jenny", "Aric"]
        npc = Player.Player(random.choice(boss_names), random.choice(["Mage","Tank", "Berserker"]), "NPC", 20)
        npc.money +=500
        npc.buy(random.choice(item for item in gamestate.items if item.cost <=200))
        npc.buy(random.choice(item for item in gamestate.items if item.cost <=200))
        npc.buy(random.choice(item for item in gamestate.items if item.cost <=200))
        for i in (npc.hp, npc.defense, npc.speed, npc.intelligence, npc.mana, npc.strength):
            i+=20
    return npc

class GameState:
    """
    
    Attributes:
        items (list of dicts of str:(dict of str:vals): All the items in the game.
            Each key is the item type; each value is a dict containing the 
            description, cost, effects (another dict of str:int), and quantity 
            of each item.
        locations ():
        travel_options ():
        location_data ():
        party (dict of Players, player name is key): all Players in a party.
        curr_location ():
        parent_location ():
    """
    def __init__(self, items, location_data, party, end_location):
        """
        """
        self.items = items
        self.end_location = end_location
        self.locations = location_data.copy()
        self.travel_options = []
        self.curr_location = "Village Square"
        self.action_options = ["shop", "encounter"]
        self.party = party
        for place in self.locations["children"][self.curr_location]:
            self.travel_options.append(place)     
            
    def new_turn(self):
        """
        """
        print(f"You are currently in {self.curr_location}")
        
        # prob needs to be command line arg but like \(i.i)/???
        action = input(f"What would you like to do? Your options are: "
                       f"{self.action_options}:")
        #add option to drink potion, give item, etc
        
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
            print(item)
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
                
    def encounter(self, initial_hp= 100):
        """An encounter with a randomly generated npc
        """
        npc = generate_npc(self)
        print("You encounter {npc.name}! They are a {npc.class} in possession of a {bag[0]}.")
        
        #npc rolls for attitude/reaction
        attitude = npc.roll_dice(20)
        print(f"{npc.name} rolling for initial impression... you rolled a {attitude}!")
        if attitude in range(7):
            print(f"You rolled low. {npc.name} is suspicious and hostile to your party.")
            action = input("Do you want to run or engage in battle? (run/battle): ")

            if action == "run":
            # do a speed check
                speed_check = self.dice(20)
                if speed_check > 10:
                    print("You successfully escape!")
                else:
                    print("Yikes. Too slow! Getting ambushed.")
                    self.battle()
            elif action == "battle":
                self.battle()

        elif attitude < 14:
            print(f"You rolled mid. {npc.name} is suspicious but ambivalent to your party.")
            print(f"{npc.name} deliberates for a minute, and ultimately gives you a clue about the final location. It starts with 'end_location[0]'")
        else:
            print(f"You rolled high. {npc.name} is not at all suspicious, and is like an old friend.")
            if npc.character_class == "Healer":
                print(f"{npc.name} is a healer! They restore your party's HP fully!")
                self.hp = self.initial_hp
            # give money
            money = npc.bag
            self.bag += money
            # recieve item
            if npc.bag: #if there are items
                give_item = random.choice(npc.bag)
                print(f"{npc.name} gives you a {give_item}!")
            
            self.bag.append(give_item)
            npc.bag.remove(give_item)  # removes the given item from NPC's bag
    
    def battle(self, status, boss=False):
        """
        """
        #1 ENEMY ONLY IM ANNOYED
        #create a queue based on speed
        #player gets option to attack, heal, defend, run, use potion
        #if status = ambush buff speed for enemy
        #if status = surprise, buff speed for players
        #neutral do nothing
        #boss battles always start neutral
        #status can be ambush (bad for player), surprise (good for player), or neutral
        debuff = 3
        npc = generate_npc(self)
        if status == "ambush":
            for player in self.party:
                self.party[player].speed -=debuff
            everyone = [self.party[p] for p in self.party]+npc
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        elif status == "surprise":
            for player in self.party:
                self.party[player].speed +=debuff
            everyone = [self.party[p] for p in self.party]+npc
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        else:
            everyone = [self.party[p] for p in self.party]+npc
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
            
    def battle_start(self, queue, npc):
        turn = 0
        while npc.hp != 0 and len(self.party) > 0:
            p = queue[turn % len(queue)]
            turn+=1
            if p.type=="Player":
                p.battle_turn_p(self, npc)
            else:
                p.battle_turn_n(self, [self.party[p] for p in self.party])
            if p.hp == 0:
                queue.remove(p)
                self.party.remove(p)
                print(f"{p.name} has died.")
        print(f"The battle has ended. {npc.name if npc.hp == 0 else 'Your party'} has lost.")
    
    def travel(self, destination):
        """
        """
        self.curr_location = destination
        self.parent_location = self.locations["parent"][self.curr_location]
        self.travel_options = [self.locations["children"][self.curr_location]]
        self.travel_options.append(self.parent_location)
        self.action_options = self.locations["locations"][self.curr_location]
        for i in range(len(self.action_options)):
            if self.action_options[i] == "b":
                self.action_options[i] = "battle"
            if self.action_options[i] == "s":
                self.action_options[i] = "shop"
            if self.action_options[i] == "e":
                self.action_options[i] = "encounter"
        self.scenario()
        
    def scenario(self):
        """Generate a scenario based on what is available at the location
        """
        options = self.locations["children"][self.curr_location]
        x = random.choice(options)
        if x == "shop":
            self.shop()
        elif x == "battle":
            self.battle()
        else:
            self.encounter()
    
    def list_party():
        pass
          
    
