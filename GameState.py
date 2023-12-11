from argparse import ArgumentParser
import Player
import json
import random
from dice import DnDRoller
import pandas as pd
import matplotlib.pyplot as plt

def generate_npc(gamestate, boss=False):
    """Generates an NPC or 'non-playable character' for humans to encounter and 
    battle. Gives name, class, items, and stats.
    Args:
        gamestate(GameState object): current state of the game that gets altered
        like items.
        boss(bool): optional boolean that notes if an NPC is boss-level
            default: False
    Returns:
        npc: the computer-generated player.
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
        item1 = gamestate.items[random.choice([item for item in gamestate.items if gamestate.items[item].cost <=200])]
        item2 = gamestate.items[random.choice([item for item in gamestate.items if gamestate.items[item].cost <=200])]
        item3 = gamestate.items[random.choice([item for item in gamestate.items if gamestate.items[item].cost <=200])]
        npc.buy(item1)
        if item1.type == "potion":
            npc.drink(item1)
        npc.buy(item2)
        if item2.type == "potion":
            npc.drink(item2)
        npc.buy(item3)
        if item3.type == "potion":
            npc.drink(item3)
        npc.hp+=20
        npc.defense+=20
        npc.speed+=20
        npc.intelligence+=20
        npc.mana+=20
        npc.strength+=20
    # for item in npc.bag:
    #     if npc.bag[item].type == "potion":
    #         npc.drink(npc.bag[item])
    return npc

class GameState:
    """State of the game. Holds the shop, new turns, encounter, battle, and the 
    randomly generated scenario that players must go through and make decisions 
    for. 
    Attributes:
        items (dict of names:Items): all the items in the game
        locations (dict): A dictionary representing the locations and 
            their connections (see map).
        travel_options (list): list of all possible travel locations based on 
            player's current location.
        party (dict of player_name:Players): all Players in a party.
        curr_location(str): Current location of player
        parent_location(str): Where player began
        dice(int): Can roll high or low for checks on speed, attitude, etc.
    """
    def __init__(self, items, location_data, party, end_location):
        """Initializes instance of GameState.
        Args:
            items (dict): A dictionary containing information about available 
            items to shop for.
            location_data (dict): A dictionary representing the locations and 
            their connections (see map).
            party (list): A list containing Player instances representing the party.
            end_location (str): name of the final destination where the boss resides.
        
        Side effects:
        """
        self.items = items
        self.dice = DnDRoller()
        self.end_location = end_location
        self.locations = location_data.copy()
        self.travel_options = []
        self.curr_location = "Village Square"
        self.action_options = ["shop", "encounter", "roll for favor"]
        self.party = party
        for place in self.locations["children"][self.curr_location]:
            self.travel_options.append(place)     
            
    def new_turn(self):
        """Initiates a new turn in the game. After one player makes a decision
        (drink, travel, etc.), either the next person in the party gets a turn
        single-player goes again. Prints the current location and available 
        action options.
        """
        if self.curr_location in self.locations["art"]:
            print(f"{self.locations['art'][self.curr_location]}")
        print(f"\nYou are currently in {self.curr_location}.")
        
        # prob needs to be command line arg but like \(i.i)/???
        if "drink" not in self.action_options:
            self.action_options.append("drink")
        if ("travel" not in self.action_options) and (self.curr_location != self.end_location):
            self.action_options.append("travel")
        if "view stats" not in self.action_options:
            self.action_options.append("view stats")
        action = input(f"What would you like to do? Your options are: "
                       f"{self.action_options}:\n")
        #add option to drink potion, give item, etc
        
        if action == 'roll for favor':
            gods_favor = self.dice.decide_advantage()
            return gods_favor
        if action == "travel":
            destination = input(f"Where would you like to go?:"
                                f"{self.travel_options}\n")
            self.travel(destination)
        elif action == "view stats":
            p = input("Please indicate which party member you wish to view, or input 'all' "
                      f"{[p for p in self.party]}: \n")
            self.list_party(name=p)
        
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
        print("\nA merchant beckons you from a nearby alley. She opens a dark box, revealing the treasures within.\n")
        for _ in range(3):
            #if you'll still have items left, leave it in the dict for now
            #otherwise, pop it for now, but if it isn't bought we'll put it back.
            item = random.choice(list(self.items))
            if self.items[item].quantity-1 != 0:
                self.items[item].quantity -= 1
                shoplist.append(self.items[item])
            else:
                shoplist.append(self.items[item])
                self.items.pop(item)
        for item in shoplist:
            print(item)
            item.stats()
            print(f"This item costs {item.cost} gold.\n")
        answer = input("Would you like to purchase an item? (y/n): ")
        if answer == "y":
            purchase = int(input("Please input the index of the item you desire: (1,2,3): "))-1
            victim = input("Please input the name of who is purchasing the item: ")
            if victim not in self.party:
                victim = input("Please input a valid name: ")
            if self.party[victim].money < shoplist[purchase].cost:
                print(f"\nYou do not have enough money for this purchase. You have {self.party[victim].money} gold.")
                print("The merchant looks at you with disgust. Those who cannot do basic math cannot purchase items.\n")
                return None
            weapons = [self.party[victim].bag[w] for w in self.party[victim].bag if self.party[victim].bag[w].type == "weapon"]
            if (len(weapons) == 1) & (shoplist[purchase].type == "weapon"):
                print("Reminder that you already have one weapon.\n"
                      "If you purchase another, you will be forced to drop one without recovering any gold.")
            confirmation = input(f"{victim} will lose {shoplist[purchase].cost} gold and gain a(n) "
                f"{shoplist[purchase].name}. Confirm purchase? (y/n): ")
            if confirmation == "y":
                #add item to player bag, subtract money, remove item from shop
                self.party[victim].buy(shoplist[purchase])
                shoplist.pop(purchase)
                print("Thank you for your purchase.\n")
                #put unsold items back
                for item in shoplist:
                    if item.name in self.items:
                        self.items[item.name].quantity +=1
                    else:
                        self.items[item.name] = item
            else:
                print("Purchase cancelled. The merchant side-eyes you and "
                    "reshuffles her wares. You sense she won't sell you anything more.\n")
                for item in shoplist:
                    if item in self.items:
                        self.items[item.name].quantity +=1
                    else:
                        self.items[item.name] = item
            self.party[victim].bag_check()
        else:
            print("The merchant side-eyes you and reshuffles her wares. "
                "She leaves as quietly as she came.\n")
        
        
    def encounter(self, initial_hp= 100):
        """An encounter with a randomly generated npc. It rolls an attitude
        check using DnDRoller, and actions spring from there to run, attack,
        recieve healing, etc.
        Args:
            initial_hp (int): initial HP value. Defaults to 100.
        """
        npc = generate_npc(self)
        print(f"\nYou encounter {npc.name}! They are a {npc.pclass} in possession of a {list(npc.bag)[0]}.\n")
        
        #npc rolls for attitude/reaction
        attitude = npc.roll_dice(20)
        print(f"{npc.name} rolling for initial impression... you rolled a {attitude}!")
        if attitude in range(10):
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
                self.battle("neutral", encounter_npc=npc)

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
                                  "Please indicate who will recieve the item: ")
            if recepient not in self.party:
                recepient = input("Please input a valid name: ")
            self.party[recepient].bag[npc.bag[give_item].name] = npc.bag[give_item]
            self.party[recepient].gift(npc.bag[give_item])
            npc.discard(npc.bag[give_item])
            self.party[recepient].bag_check()
            
    
    def battle(self, status, boss=False, encounter_npc=None):
        """Starts a battle sequence if player chooses or gets ambushed.
        Args:
            status (str): status of the battle, which can be "ambush," "surprise,"
            or "neutral."
            boss (bool): Indicates if the encounter is a boss battle. 
            Defaults to False.
            encounter_npc(obj): NPC instance for the encounter. Defaults to None, but
            will be generated.
        Side effects:
            Modifies the speed attribute of players in the party based on the battle status.
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
        if encounter_npc == None:
            npc = generate_npc(self, boss)
        else:
            npc = encounter_npc
        
        if status == "ambush":
            for player in self.party:
                self.party[player].speed -=debuff
            if len(self.party) > 1:
                everyone = [self.party[p] for p in self.party]+[npc]
            else:
                everyone = [self.party.get(list(self.party)[0]),npc]
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        elif status == "surprise":
            for player in self.party:
                self.party[player].speed +=debuff
            if len(self.party) > 1:
                everyone = [self.party[p] for p in self.party]+[npc]
            else:
                everyone = [self.party.get(list(self.party)[0]),npc]
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
        
        else:
            if len(self.party) > 1:
                everyone = [self.party[p] for p in self.party]+[npc]
            else:
                everyone = [self.party.get(list(self.party)[0]),npc]
            queue = sorted(everyone, key= lambda s: s.speed)
            self.battle_start(queue, npc)
            
    def battle_start(self, queue, npc):
        """Initiates the turn-based battle sequence between the player(s) and NPC.
        Args:
            queue (list): Representing the turn order of battle. Based on speed stat.
            npc (obj): NPC acting opponent.
        Side effects:
            Modifies the state of the game based on the outcomes of each turn.
            Prints battle, like HP losses, moves, etc.
        """
        turn = 0
        self.mathematician_save = self.party.copy()
        self.list_party()
        self.list_party(npc=npc)
        hp_track = {'Turn': [], 'NPC_HP': []}
        for player in self.party:
            hp_track[f"{player}_HP"] = []
        #debug
        while npc.hp > 0 and len(self.party) > 0 and len(queue) >1:
            p = queue[turn % len(queue)]
            turn+=1
            
            hp_track['Turn'].append(turn)
            for player in self.party:
                if self.party[player].hp >= 0:
                    hp_track[f"{player}_HP"].append(self.party[player].hp)
                else:
                    hp_track[f"{player}_HP"].append(0)
                #hp_track['Player_HP'].append(self.party['Player'].hp if 'Player' in self.party else 0)
            hp_track['NPC_HP'].append(npc.hp)
            
            if p.type=="Player":
                if p.hp > 0:
                    if p.battle_turn_p(self, npc) == False:
                        queue.remove(p)
                else:
                    if p in queue:
                        queue.remove(p)
                    self.party.pop(p.name)
                    print(f"{p.name} has died.")
            else:
                if len(queue) == 1:
                    pass
                else:
                    p.battle_turn_n(self, [p for p in queue if p.type!="NPC"])
            
        print(f"The battle has ended. {npc.name if npc.hp <= 0 else 'Your party'} has lost.")
        if npc.hp <= 0:
            print("You reap the spoils of the battle! Gain 50 gold per person.")
            for p in self.party:
                self.party[p].money+=50
                
        self.mathematician(hp_track)
    
    def mathematician(self, hp_track):
        """Track and plot the HP changes."""
        print("A lone figure stands in the distance, robes flowing even though there is no wind. Approach them.")
        print("Close plot to continue")
        for x in hp_track:
            if len(hp_track[x]) < len(hp_track['Turn']):
                hp_track[x]+=[0]*(len(hp_track['Turn'])-len(hp_track[x]))
            
        hp_df = pd.DataFrame(hp_track)
            
        for player in self.mathematician_save:
            plt.plot(hp_df['Turn'], hp_df[f"{player}_HP"], label=f"{player} HP")
        plt.plot(hp_df['Turn'], hp_df['NPC_HP'], label='NPC HP')
        plt.xlabel('Turn')
        plt.ylabel('HP')
        plt.legend()
        plt.title('HP as Battle Progresses')
        plt.show()

    def travel(self, destination):
        """Changes the location of the player to the specified destination
        backwards or forwards. Then updates current location, travel options,
        and the actions available.
        Args:
            destination (str): The name of the destination location.
        """
        self.curr_location = destination
        if self.curr_location in self.locations["parent"]:
            self.parent_location = self.locations["parent"][self.curr_location]
        self.travel_options = []
        if self.curr_location in self.locations["children"]:
            for locale in self.locations["children"][self.curr_location]:
                self.travel_options.append(locale)
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
        """Generate a scenario based on what the player selects.
        Args:
            action (str): The player's selected action.
        """
        if action == "shop":
            self.shop()
        elif action == "battle":
            self.battle("surprise")
        elif action == "encounter":
            self.encounter()
        elif action == "drink":
            drinker = input("You have chosen to drink a potion. Who will be drinking? ")
            if drinker not in self.party:
                drinker = input("Please select someone in the party: ")
                # breaks if you don't select someone in party again or say `no`
            x = self.party[drinker].view_bag()
            print(x)
            print("Listed are the items in your bag.")
            if x == []:
                print("You have no items to drink.")
                return None
            print(f"{drinker} will be drinking the potion! ")
            potion_name = input("Please indicate which potion you wish to consume "
                                "or input 'cancel': ")
            if (potion_name != "cancel") & (potion_name in self.party[drinker].bag):
                drinker = self.party[drinker]
                death = drinker.drink(drinker.bag[potion_name])
                if death != False:
                    print(f"Successfully drank {potion_name}")
                    self.list_party(drinker.name)
                else:
                    self.list_party(drinker.name)
                    self.party.pop(drinker.name)
            elif potion_name != "cancel":
                potion_name = input("Please input a valid potion: ")
                drinker = self.party[drinker]
                death = drinker.drink(drinker.bag[potion_name])
                if death != False:
                    print(f"Successfully drank {potion_name}")
                    self.list_party(drinker.name)
                else:
                    self.list_party(drinker.name)
                    self.party.pop(drinker.name)
        else:
            print("\nYou have angered the gods. Choose from your available options. ")
            self.new_turn()
            
            
    
    def list_party(self, name="all", npc=None):
        """Lists stats for party.
        Args:
            name (str): The name of the party member. Defaults to "all".
            npc (Player): An optional NPC instance. Defaults to None.
        """
        if name != "all" and npc == None:
            player = self.party[name]
            print(player)
        elif npc != None:
            print(npc)
        else:
            for p in self.party:
                player = self.party[p]
                print(player)
    