
class Item:
    """
    """
    def __init__(self):
        self.description = ""
        self.type = "" #potion, armor, weapon
        self.cost = 1
        self.effects = {} #dictionary within individual item dictionaries with 
                          #listed changes to person's stats
        self.name = ""
        self.quantity
    def stats(self):
        print(f"This is a {self.name}. Its effects are: ")
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")