'''a player in the game
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
from typing import Any


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
    def __init__(self, name, pclass):
        self.name=name
        self.pclass=pclass
        self.hp, self.strength, self.speed, self.mana, \
            self.intelligence, self.defense = class_stats[pclass]
        self.bag = []
        self.money = 100
    def attack(self, enemy):
        pass
    def defend(self, ally):
        pass
    def buy(self, item):
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
    def give(self, item):
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
        pass
# nicole = Player("nicole", "Healer")
# print(nicole.intelligence)

