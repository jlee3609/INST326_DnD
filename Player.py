'''a player in the game
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
from dice import DnDRoller

#a problem for later
class_stats = {
    "Mage": [5,5,5,5,5,5],
    "Healer": [5,5,5,5,5,5],
    "Tank": [5,5,5,5,5,5],
    "Assassin": [5,5,5,5,5,5],
    "Berserker": [5,5,5,5,5,5]
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
        bag (list): player's inventory
    '''
    def __init__(self, name, pclass, dice):
        self.name=name
        self.pclass=pclass
        self.dice = dice
        self.hp, self.strength, self.speed, self.mana, \
            self.intelligence, self.defense = class_stats[pclass]
        self.bag = []
        self.money = 100
    def attack(self, enemy):
        weapon_info = data.get('weapons', {}).get(weapon) #calls the json file that will be added later
        dice = weapon_info.get('dice') #the dice associated with each weapon
        # if method?
    
    def defend(self, ally):
        pass
    
    def item_effects(self, item, action):
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
    def buy(self, item):
        if len(self.bag) > 10:
            raise Exception("Your bag can only carry so much. Drink or use an"
                            "item to continue purchase.")
        else:
            self.bag.append(item)
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
        self.bag.remove(item)
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
        
    def drink(self, item):
        if item.type == "potion":
            self.bag.remove(item)
        else:
            #if you were dumb enough to drink a sword/shield you deserve it
            self.hp -= 50
    def roll_dice(self, dice_num):
        vibes = DnDRoller.roll(self.dice)
    
    def battle_turn(self):
        
    
# nicole = Player("nicole", "Healer")
# print(nicole.intelligence)
