'''a player in the game (npc or human)
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
from dice import DnDRoller

#default class stats
class_stats = {
    "Mage": [100,5,10,20,5,5],
    "Healer": [100,10,5,20,5,5],
    "Tank": [100,5,5,5,5,10],
    "Assassin": [100,5,20,5,5,5],
    "Berserker": [100,20,5,5,0,10]
}
class Player:
    '''A player
    
    Attributes:
            name (str): player name
            pclass (str): player class (mage, tank, etc)
            hp (int): player's hp from pclass
            strength (int): player's strength from pclass
            speed (int): player's speed from pclass
            mana (int): player's mana from pclass
            intelligence (int): player's intelligence from pclass
            defense (int): player's defense from pclass
            money (int): player's money, starts at 100
            bag (dict): player's inventory
            armor (bool): existing defenses/armors, defaults at 0
            dice (DnDRoller): A dice object belonging to each player

    '''
    def __init__(self, name, pclass, type):
        """Initializes player's character instance.
        
        Args:
            name (str): player name
            pclass (str): player class (mage, healer, tank, assassin, berserker)
            type (str): whether the player is a player or an npc
        
        Side effects:
            Sets `name`, `type`, `pclass`, `dice`, all `stats`, `bag`, `money`, 
                and `armor` attributes
        """
        self.name=name
        self.type=type
        self.pclass=pclass
        self.dice = DnDRoller()
        stats = class_stats.get(pclass, (0, 0, 0, 0, 0, 0))
        self.hp, self.strength, self.speed, self.mana, \
            self.intelligence, self.defense = stats
        self.bag = {}
        self.money = 100
        self.armor = 0
    
    def __str__(self):
        """F-string representing the character's attributes and possessions informally.
        
        Returns:
            f-string: informal string of all a player's attributes
        """
        #list out player attributes
        return(f"""
               {self.name}:
               Attributes:
               Class - {self.pclass}
               HP - {self.hp}
               Strength - {self.strength}
               Speed - {self.speed}
               Mana - {self.mana}
               Intelligence - {self.intelligence}
               Defense - {self.defense}
               
               Posessions:
               Money - {self.money}
               Items - {self.view_bag()}
               """)
    
    def view_bag(self, category="all"):
        """View the items in the character's bag, optionally filtered by category.
        
        Args:
            category (str): category of items like potions. Default is "all".
            
        Returns:
            bag (list): Writes out player's items and item descriptions.
        """
        bag = []
        if category != "all":
            bag_items = [self.bag[i] for i in self.bag if self.bag[i].type == category]
            for item in bag_items:
                bag.append(str(item)+" "+str(item.effects))
        else:
            bag_items = [self.bag[i] for i in self.bag]
            for item in bag_items:
                bag.append(str(item)+" "+str(item.effects))
        return bag
    
    
    def attack(self, enemy, npc = False):
        """Perform an attack on an enemy with weapons from bag. If no weapons,
        will hit with bare fists.
        
        Args:
            enemy (Player): enemy player to attack.
            npc (bool): Whether it's an npc attacking (will not print some strings)
                Default: False.
        
        Side effects:
            Prints to terminal
            Changes enemy hp attribute based on damage done by self.
        """
        if self.pclass == "Mage":
            attack = self.mana
        else:
            attack = self.strength
        #account for if the player has no weapon
        weapons = [self.bag[w] for w in self.bag if self.bag[w].type == "weapon"]
        if weapons != []:
            weapon = weapons[0]
            net_dmg = enemy.defense-weapon.damage-attack \
                if enemy.defense<(attack+weapon.damage) else 0
            print(f"{self.name} uses their {weapon.name} to attack {enemy.name}!")
        else:
            if not npc:
                print(f"You attempt to hit {enemy.name} with your bare fists."
                  " Unfortunately, you can only deal 5 bonus HP dmg.")
            net_dmg = enemy.defense-5-attack if enemy.defense<(5+attack) \
            else 0
        enemy.hp+=net_dmg
        print(f"{self.name} hit {enemy.name} for {net_dmg} HP! They now have {enemy.hp} HP.")
            

    def heal(self, ally):
        """Healing or restoring HP. If class is healer, player can heal self or 
        others based on mana level. If not, heals only 1 hp.
        
        Args:
            ally (Player): Party member that can be healed.
            
        Side effects:
            Prints to terminal
            Adds to ally.hp
        """
        if self.pclass == "Healer":
            print("As you are a healer, you heal based on mana level. ")
            heal = round(1.5*self.mana)
            ally.hp+=heal
            print(f"{ally.name} healed {heal} HP! They now have {ally.hp} HP.")
        else:
            print("As you are not a healer, you may heal a paltry 1 HP.")
            ally.hp+=1
            print(f"{ally.name} healed 1 HP! They now have {ally.hp} HP.")
            
    def defend(self):
        """Defend self with armor from bag. For one turn, if hit, will lose less HP than if 
        they had no armor.
        
        Side effects:
            Prints to terminal
            Changes armor attribute to total defense from armor from bag, adds armor to
            self.defense
        
        """
        armor = [self.bag[w] for w in self.bag if self.bag[w].type == "armor"]
        print(armor)
        total_armor = 5
        for a in armor:
            print(a)
            total_armor-=a.damage
            print(total_armor)
        self.defense += total_armor
        self.armor = total_armor
        print(f"You bolster your defenses! You add {total_armor} to your defense until the next turn.")
    
    
    def buy(self, item):
        """From shop, the ability to buy items. Bag size is 5, 
        buying more will prompt user to discard an item. 
        
        Args:
            item (Item): Item object being purchased by player
            
        Side effects:
            Print to terminal
            Add item to self.bag
            calls discard(): Potentially discard one item from self.bag
            If item is not potion, adds to stat attributes based on item stats
        """
        if len(self.bag) == 5:
            print(self.view_bag())
            discard = input("Your bag can only carry so much. Drink or use an "
                            "item to continue purchase.")
            self.discard(item)
        else:
            self.bag[item.name] = item
            self.money -= item.cost
            if item.type != "potion":
                if "hp" in item.effects:
                    self.hp += item.effects["hp"]
                if "strength" in item.effects:
                    self.strength += item.effects["strength"]
                if "speed" in item.effects:
                    self.speed += item.effects["speed"]
                if "mana" in item.effects:
                    self.mana += item.effects["mana"]
                if "intelligence" in item.effects:
                    self.intelligence += item.effects["intelligence"]
                if "defence" in item.effects:
                    self.defense += item.effects["defense"]
    
    def gift(self, item):
        """Be gifted an item to alter stats. Given to self.
        
        Args:
            item (Item): item being give to self
            
        Side effects:
            Adds item stats to player stats if item is not potion 
            (if potion, must wait to drink)
            Adds item to bag
        """
        self.bag[item.name] = item
        if item.type != "potion":
            if "hp" in item.effects:
                self.hp += item.effects["hp"]
            if "strength" in item.effects:
                self.strength += item.effects["strength"]
            if "speed" in item.effects:
                self.speed += item.effects["speed"]
            if "mana" in item.effects:
                self.mana += item.effects["mana"]
            if "intelligence" in item.effects:
                self.intelligence += item.effects["intelligence"]
            if "defence" in item.effects:
                self.defense += item.effects["defense"]
                
    def discard(self, item):
        """Discards item from self.bag, losing its effects as well if it's not a potion.
        As potions are drinkable, if the item is still in the bag it has not affected player stats.
        
        Args:
            item (Item): item to be discarded
            
        Side effects:
            Removes item stats to player stats if item is not potion 
            (if potion, being in the bag had no effects on player stats)
            Removes item from bag
        """
        if item.type != "potion":
            if "hp" in item.effects:
                self.hp -= item.effects["hp"]
            if "strength" in item.effects:
                self.strength -= item.effects["strength"]
            if "speed" in item.effects:
                self.speed -= item.effects["speed"]
            if "mana" in item.effects:
                self.mana -= item.effects["mana"]
            if "intelligence" in item.effects:
                self.intelligence -= item.effects["intelligence"]
            if "defence" in item.effects:
                self.defense -= item.effects["defense"]
        self.bag.pop(item.name)

    def drink(self, item):
        """Ability to drink anything. Potions, weapons, whatever.
        
        Args:
            item (Item): item to be drank
        
        Side effects:
            calls discard(): Removes item from bag
            Prints to terminal
            Changes player stats based on potion stats
        
        Returns:
            False if player dies while drinking potion
        """
        if item.type == "potion":
            del self.bag[item.name]
            if "hp" in item.effects:
                    self.hp += item.effects["hp"]
            if "strength" in item.effects:
                self.strength += item.effects["strength"]
            if "speed" in item.effects:
                self.speed += item.effects["speed"]
            if "mana" in item.effects:
                self.mana += item.effects["mana"]
            if "intelligence" in item.effects:
                self.intelligence += item.effects["intelligence"]
            if "defence" in item.effects:
                self.defense += item.effects["defense"]
        else:
            #if you were dumb enough to drink a sword/shield you deserve it
            print("The gods of DnD look on with disdain "
                  "as you attempt to consume what should not be consumed. "
                      "You lose both the item and 50 HP.")
            self.discard(item)
            self.hp -= 50
        if self.hp <= 0:
            return False
    
    def roll_dice(self, dice_num):
        """Calls the roll_sets method from dice.py class DnDRoller to roll dice
        Args:
            dice_num (int): number of sides (4, 6, 8, 10, 12, 20).
        Returns:
            the result of the roll (int)
        """
        roll = self.dice.roll_sets(dice_num)
        return roll
    
    def battle_turn_p(self, gamestate, npc):
        """Take a player turn in battle. Choose action like attack, heal, etc. 
        
        Args:
            gamestate (GameState): game object containing party, etc
            npc (Player): npc enemy
            
        Side effects:
            Prints to terminal
            Potentially:
                calls defend(): Changes armor and defense stats
                calls heal(): Adds to HP stat (ally or self)
                calls attack(): Removes HP from npc
                Escapes from battle (remove player from queue)
                calls drink(): Consumes item (drink item) and removes item from bag
        Returns:
            False if player succeeds speed check and escapes from battle
                
        
        """
        print(f"It's {self.name}'s turn.")
        turn = input("Please choose an action: Attack, Heal, Defend, Run, Drink:\n")
        if turn == "Attack":
            self.defense-=self.armor
            self.armor = 0
            self.attack(npc)
        elif turn == "Heal":
            self.defense-=self.armor
            self.armor = 0
            ally = input(f"Please indicate who you want to heal: {[p for p in gamestate.party]}")
            while ally not in gamestate.party:
                print("Please input a valid player.")
                ally = input(f"Please indicate who you want to heal: {[p for p in gamestate.party]}")
            self.heal(gamestate.party[ally])
        elif turn == "Defend":
            #defends extra if they have armor, otherwise only defends 5 extra from base stats
            self.defend()

        elif turn == "Run":
            self.defense-=self.armor
            self.armor = 0
            if self.dice.roll_sets(20+self.speed) >= self.dice.roll_sets(20+npc.speed):
                print(f"You outspeed {npc.name} and escape!")
                return False
            else:
                self.hp-=5
                print(f"You fail to escape battle and lose 5 HP as you are dragged back.")
        elif turn == "Drink":
            drinker = input("You have chosen to drink a potion.")
            x = self.view_bag()
            
            if x != []:
                print(x)
                print("Listed are the items in your bag.")
                potion_name = input("Please indicate which item you wish to consume or input cancel: ")
                if potion_name != "cancel":
                    while potion_name not in self.bag:
                        potion_name = input("Please indicate an item in your bag: ")
                    death = self.drink(self.bag[potion_name])
                    if death!=False:
                        print(f"Successfully drank {potion_name}")
                        gamestate.list_party(self.name)
                    else:
                        print(f"You died from drinking {potion_name}.")
                        gamestate.list_party(self.name)
                        gamestate.party.pop(self.name)
                    
            else:
                print("You have no items to drink.")
            
        else:
            print("Please input a valid action.")
            self.battle_turn_p(gamestate, npc)
        pass
    
    def battle_turn_n(self, party):
        """Take a npc turn in battle. Automatically attacks player with lowest hp. 
        
        Args:
            party (dict of Players): self.party from the current gamestate, 
                                    all the players currently in battle
        
        Side effects:
            Prints to terminal
            Attacks player with lowest HP, player.hp stat drops
        """
        print(f"It's {self.name}'s turn.")
        hp_sort = sorted(party, key= lambda p: p.hp)
        self.attack(hp_sort[0], npc=True)
        
    
    def bag_check(self):
        """Checks the bag of the player. Only 5 items, only one weapon allowed.
        
        Side effects:
            Prints to terminal
            calls discard(): Potentially removes item from bag
        """
        weapons = [self.bag[w] for w in self.bag if self.bag[w].type == "weapon"]
        if len(weapons)>1:
            print("You can only carry one weapon at a time. "
                    "Please choose a weapon to discard!")
            print(self.view_bag("weapon"))
            discard = input("Weapon name: ")
            self.bag.pop(discard)
        if len(self.bag) > 5:
            print(self.view_bag())
            discard = input("Your bag can only carry so much. "
                  "Drink or discard an item to continue: ")
            self.bag.pop(discard)
