from argparse import ArgumentParser
import Player
import json
import random
from dice import DnDRoller

def generate_npc(gamestate, boss=False):
    """
    """
    names = ["Aeliana", "Thoren", "Elowen", "Kael", "Seraphim", "Lirael", "Garrick", 
            "Isabeau", "Eldon", "Lyria", "Caden", "Rowena", "Thaddeus", "Anara",
            "Finnian", "Livia", "Dorian", "Tamsin", "Galadriel", "Merek"]
    classes = ["Mage", "Healer", "Tank", "Assassin", "Berserker"]
    if boss == False:
        npc = Player.Player(random.choice(names), random.choice(classes), "NPC")
        npc.buy(gamestate.items[random.choice([item for item in gamestate.items if gamestate.items[item].cost <=100])])
    else:
        boss_names = ["Nicole", "Ariel", "Jenny", "Aric"]
        npc = Player.Player(random.choice(boss_names), random.choice(["Mage","Tank", "Berserker"]), "NPC")
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
        items (dict of Items, keys are names and values are the Item): all the items in the game
        locations ():
        travel_options ():
        location_data ():
        party (dict of Players, player name is key): all Players in a party.
        curr_location ():
        parent_location ():
        dice ():
    """
    def __init__(self, items, location_data, party, end_location):
        """
        """
        self.items = items
        self.dice = DnDRoller()
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
        
        #  \(i.i)/???
        self.action_options = self.action_options+["drink","travel"]
        action_opt_str = ""
        for action in self.action_options:
            action_opt_str += action
        action = input(f"What would you like to do? Your options are: "
                       f"{action_opt_str}:\n")
        #add option to drink potion, give item, etc
        
        if action == "travel":
            destination = input(f"Where would you like to go?:"
                                f"{self.travel_options}\n")
            self.travel(destination)
        else:
            self.scenario(action)
        
    def shop(self):
        """Opens up a shop that one item can be purchased from
        
        Side effects:
            Potentially removes 1 item from items dictionary
            Potentially adds 1 item to 1 player's bag
            Potentially removes gold from 1 player's money
            Prints to terminal
        
        """
        shoplist = []
        print("A merchant beckons you from a nearby alley. She opens a dark box, revealing the treasures within.")
        for _ in range(3):
            #if you'll still have items left, leave it in the dict for now
            #otherwise, pop it for now, but if it isn't bought we'll put it back.
            item =random.choice(list(self.items))
            if self.items[item].quantity-1 != 0:
                self.items[item].quantity -= 1
                shoplist.append(self.items[item])
            else:
                shoplist.append(self.items[item])
                self.items.pop(item)
        for item in shoplist:
            print(item)
            item.stats()
            print(f"This item costs {item.cost} gold.")
        answer = input("Would you like to purchase an item? (y/n)")
        if answer == "y":
            purchase = int(input("Please input the index of the item you desire: (1,2,3)"))-1
            victim = input("Please input the name of who is purchasing the item:")
            if victim not in self.party:
                victim = input("Please input a valid name:")
            if self.party[victim].money < shoplist[purchase].cost:
                print(f"You do not have enough money for this purchase. You have {self.party[victim].money} gold.")
                print("The merchant looks at you with disgust. Those who cannot do basic math cannot purchase items.")
                return None
            confirmation = input(f"{victim} will lose {shoplist[purchase].cost} and gain a(n) "
                f"{shoplist[purchase].name}. Confirm purchase? (y/n)")
            if confirmation == "y":
                #add item to player bag, subtract money, remove item from shop
                self.party[victim].buy(shoplist[purchase])
                shoplist.pop(purchase)
                print("Thank you for your purchase.")
                #put unsold items back
                for item in shoplist:
                    if item.name in self.items:
                        self.items[item.name].quantity +=1
                    else:
                        self.items[item.name] = item
            else:
                print("Purchase cancelled. The merchant side-eyes you and "
                    "reshuffles her wares. You sense she won't sell you anything more.")
                for item in shoplist:
                    if item in self.items:
                        self.items[item.name].quantity +=1
                    else:
                        self.items[item.name] = 1
        else:
            print("The merchant side-eyes you and reshuffles her wares. \
                She leaves as quietly as she came.")
                
    def encounter(self, initial_hp= 100):
        """An encounter with a randomly generated npc
        """
        npc = generate_npc(self)
        print(f"You encounter {npc.name}! They are a {npc.pclass} in possession of a {list(npc.bag)[0]}.")
        
        #npc rolls for attitude/reaction
        attitude = npc.roll_dice(20)
        print(f"{npc.name} rolling for initial impression... you rolled a {attitude}!")
        if attitude in range(7):
            print(f"You rolled low. {npc.name} is suspicious and hostile to your party.")
            action = input("Do you want to run or engage in battle? (run/battle): ")

            if action == "run":
            # do a speed check
                max_speed = max([self.party[p].speed for p in self.party])
                speed_check = self.dice.roll_sets(20+max_speed)
                if speed_check > npc.speed:
                    print("You successfully escape!")
                else:
                    print("Yikes. Too slow! Getting ambushed.")
                    self.battle("ambush")
            elif action == "battle":
                self.battle("neutral")

        elif attitude < 14:
            print(f"You rolled mid. {npc.name} is suspicious but ambivalent to your party.")
            print(f"{npc.name} deliberates for a minute, and ultimately gives you a clue about the final location. It starts with {self.end_location[0]}")
        else:
            print(f"You rolled high. {npc.name} is not at all suspicious, and is like an old friend.")
            if npc.pclass == "Healer":
                print(f"{npc.name} is a healer! They restore your party's HP fully!")
                self.hp = initial_hp
                return None
            # give money
            money = round(npc.money/len(self.party))
            for player in self.party:
                self.party[player].money += money
            print(f"{npc.name} gives everyone {money} gold!")
            # recieve item
            give_item = random.choice(list(npc.bag))
            recepient = input(f"{npc.name} gives you a {npc.bag[give_item].name}! "
                                  "Please indicate who will recieve the item:")
            self.party[recepient].bag[npc.bag[give_item].name] = npc.bag[give_item]
            npc.give(self.party[recepient], npc.bag[give_item])
            #npc.bag.pop(give_item)  # removes the given item from NPC's bag
    
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
        npc = generate_npc(self, boss)
        
        if status == "ambush":
            for player in self.party:
                self.party[player].speed -=debuff
            everyone = [self.party[p] for p in self.party].append(npc)
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        elif status == "surprise":
            for player in self.party:
                self.party[player].speed +=debuff
            everyone = [self.party[p] for p in self.party] #.append(npc)
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        else:
            if len(self.party) > 1:
                everyone = [self.party[p] for p in self.party].append(npc)
            else:
                everyone = [self.party.get(list(self.party)[0]),npc]
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
            
    def battle_start(self, queue, npc):
        turn = 0
        while npc.hp != 0 and len(self.party) > 0:
            p = queue[turn % len(queue)]
            turn+=1
            if p.type=="Player":
                if p.battle_turn_p(self, npc) == False:
                    queue.remove(p)
            else:
                p.battle_turn_n(self, [self.party[p] for p in self.party])
            if p.hp == 0:
                queue.remove(p)
                self.party.remove(p)
                print(f"{p.name} has died.")
        print(f"The battle has ended. {npc.name if npc.hp == 0 else 'Your party'} has lost.")
        if npc.hp == 0:
            print("You reap the spoils of the battle! Gain 50 gold per person.")
            for p in self.party:
                self.party[p].money+=50
    
    def travel(self, destination):
        """
        """
        self.curr_location = destination
        self.parent_location = self.locations["parent"][self.curr_location]
        self.travel_options = self.locations["children"][self.curr_location]
        self.travel_options.append(self.parent_location)
        self.action_options = self.locations["locations"][self.curr_location]
        for i in range(len(self.action_options)):
            if self.action_options[i] == "b":
                self.action_options[i] = "battle"
            if self.action_options[i] == "s":
                self.action_options[i] = "shop"
            if self.action_options[i] == "e":
                self.action_options[i] = "encounter"
        
    def scenario(self, action):
        """Generate a scenario based on what the player selects
        """
        if action == "shop":
            self.shop()
        elif action == "battle":
            self.battle("surprise")
        elif action == "encounter":
            self.encounter()
        else:
            drinker = input("You have chosen to drink a potion. Who will be drinking? ")
            x = self.party[drinker].view_bag(category='potion')
            print("Listed are the potions in your bag.")
            if x == []:
                print("You have no potions to drink.")
                return None
            potion_name = input(f"{drinker} will be drinking the potion! "
                f"Please indicate which potion you wish to consume: ")
            drinker = self.party[drinker]
            drinker.drink(drinker.bag[potion_name])
            print(f"Successfully drank {potion_name}")
            self.list_party(drinker.name)
    
    def list_party(self, name=None):
        if name != None:
            player = self.party[name]
            print(player)
        else:
            for p in self.party:
                player = self.party[p]
                print(player)
    
