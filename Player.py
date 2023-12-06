'''a player in the game
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
from dice import DnDRoller

#a problem for later
class_stats = {
    "Mage": [100,5,5,5,5,5],
    "Healer": [100,5,5,5,5,5],
    "Tank": [100,5,5,5,5,5],
    "Assassin": [100,5,5,5,5,5],
    "Berserker": [100,5,5,5,5,5]
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
        self.armor = False
    
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
        bag = []
        if category != "all":
            bag_items = [self.bag[i] for i in self.bag if self.bag[i].type == category]
            for item in bag_items:
                print(item)
                print(item.effects)
                bag.append(str(item)+"\n"+str(item.effects))
        else:
            for item in self.bag:
                print(item)
                print(item.effects)
                bag.append(str(item)+"\n"+item.effects)
        return bag
    
    
    #?????
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
                  "Unfortunately, you can only deal 5 bonus HP dmg.")
            net_dmg = enemy.defense-5-attack if enemy.defense<(5+attack) \
            else 0
        enemy.hp+=net_dmg
        print(f"{self.name} hit {enemy.name} for {net_dmg} HP! They now have {enemy.hp} HP.")
            

    def heal(self, ally):
        if self.pclass == "Healer":
            print("As you are a healer, you heal based on mana level.")
            heal = round(0.5*self.mana)
            ally.hp+=heal
            print(f"{ally.name} healed {heal} HP! They now have {ally.hp} HP.")
        else:
            print("As you are not a healer, you may heal a paltry 1 HP.")
            ally.hp+=1
            print(f"{ally.name} healed {heal} HP! They now have {ally.hp} HP.")
            
    def defend(self):
        armor = [self.bag[w] for w in self.bag if self.bag[w].type == "armor"]
        total_armor = 0
        for a in armor:
            total_armor-=a.damage
        self.defense += total_armor
        self.armor = True
        print(f"You bolster your defenses! You add {total_armor} to your defense until the next turn.")
    
    # def item_effects(self, item, action):
    #     if item.type != "potion":
    #             if "hp" in item.effects:
    #                 self.hp += item.effects["hp"]
    #             if "strength" in item.effects:
    #                 self.strength += item.effects["strength"]
    #             if "speed" in item.effects:
    #                 self.speed += item.effects["speed"]
    #             if "mana" in item.effects:
    #                 self.mana += item.effects["mana"]
    #             if "intelligence" in item.effects:
    #                 self.intelligence += item.effects["intelligence"]
    #             if "defence" in item.effects:
    #                 self.defense += item.effects["defense"]
    
    def buy(self, item):
        if len(self.bag) > 10:
            raise Exception("Your bag can only carry so much. Drink or use an"
                            "item to continue purchase.")
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
    
    def give(self, other_player, item):
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
            print("The gods of DnD look on with disdain \
                  as you attempt to consume what should not be consumed. \
                      You lose both the item and 50 HP.")
            del self.bag[item.name]
            self.hp -= 50
    
    def roll_dice(self, dice_num):
        roll = self.dice.roll_sets(dice_num)
        return roll
    
    def battle_turn_p(self, gamestate, npc):
        print(f"It's {self.name}'s turn.")
        turn = input("Please choose an action: Attack, Heal, Defend, Run, Drink:\n")
        if turn == "Attack":
            self.armor=False
            self.attack(npc)
        elif turn == "Heal":
            self.armor=False
            ally = input(f"Please indicate who you want to heal: {[p for p in self.party]}")
            self.heal(self.party[ally])
        elif turn == "Defend":
            #defends extra if they have armor, otherwise only defends 1 extra from base stats
            self.defend()

        elif turn == "Run":
            self.armor = False
            if self.speed >= npc.speed:
                print(f"You outspeed {npc.name} and escape!")
                return False
            else:
                self.hp-=5
                print(f"You fail to escape battle and lose 5 HP as you are dragged back.")
        else:
            print("Please input a valid action.")
            self.battle_turn(npc)
        pass
    def battle_turn_n(self, gamestate, party):
        print(f"It's {self.name}'s turn.")
        hp_sort = sorted(party, key= lambda p: p.hp)
        self.attack(hp_sort[0], npc=True)
        pass
# nicole = Player("nicole", "Healer")
# print(nicole.intelligence)