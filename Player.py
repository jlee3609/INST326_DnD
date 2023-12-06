'''a player in the game
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
from dice import DnDRoller

#a problem for later
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
        hp (int): player's hp
        strength (int): player's strength
        speed (int): player's speed
        mana (int): player's mana
        intelligence (int): player's intelligence
        defense (int): player's defense
        money (int): player's money
        bag (dict): player's inventory
        armor (bool): whether a player is defending
    '''
    def __init__(self, name, pclass, type):
        self.name=name
        self.type=type
        self.pclass=pclass
        self.dice = DnDRoller()
        self.hp, self.strength, self.speed, self.mana, \
            self.intelligence, self.defense = class_stats[pclass]
        self.bag = {}
        self.money = 100
        self.armor = 0
    
    def __str__(self):
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
        #print("start bag")
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
        else:
            if not npc:
                print(f"You attempt to hit {enemy.name} with your bare fists."
                  " Unfortunately, you can only deal 5 bonus HP dmg.")
            net_dmg = enemy.defense-5-attack if enemy.defense<(5+attack) \
            else 0
        enemy.hp+=net_dmg
        print(f"{self.name} hit {enemy.name} for {net_dmg} HP! They now have {enemy.hp} HP.")
            

    def heal(self, ally):
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
        armor = [self.bag[w] for w in self.bag if self.bag[w].type == "armor"]
        total_armor = 5
        for a in armor:
            total_armor-=a.damage
        self.defense += total_armor
        self.armor = total_armor
        print(f"You bolster your defenses! You add {total_armor} to your defense until the next turn.")
    
    
    def buy(self, item):
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
    
    def roll_dice(self, dice_num):
        roll = self.dice.roll_sets(dice_num)
        return roll
    
    def battle_turn_p(self, gamestate, npc):
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
            #defends extra if they have armor, otherwise only defends 1 extra from base stats
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
                    self.drink(self.bag[potion_name])
                    print(f"Successfully drank {potion_name}")
                    gamestate.list_party(self.name)
            else:
                print("You have no items to drink.")
            
        else:
            print("Please input a valid action.")
            self.battle_turn_p(gamestate, npc)
        pass
    def battle_turn_n(self, gamestate, party):
        print(f"It's {self.name}'s turn.")
        hp_sort = sorted(party, key= lambda p: p.hp)
        self.attack(hp_sort[0], npc=True)
        pass
    
    def bag_check(self):
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
            
            
# nicole = Player("nicole", "Healer")
# print(nicole.intelligence)
