'''a player in the game
'''

# stat order = HP, Strength, Speed, Mana, Intelligence, Defense
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
        bag (list): player's inventory
    '''
    def __init__(self, name, pclass):
        self.name=name
        self.pclass=pclass
        self.hp, self.strength, self.speed, self.mana, \
            self.intelligence, self.defense = class_stats[pclass]
        self.bag = []
    def attack(self, enemy):
        pass
    def defend(self, ally):
        pass
    def buy(self, item):
        #ooh this coule get complicated ill handle this one
        pass
    def drink(self, item):
        pass
    def roll_dice(self, dice_num):
        pass
        
# nicole = Player("nicole", "Healer")
# print(nicole.intelligence)