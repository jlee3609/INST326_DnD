
class Item:
    def __init__(self):
        self.type = ""
        self.cost = 1
        self.effects = {} #stat, number
        self.name = ""
    def stats(self):
        print(f"This is a {self.name}. Its effects are: ")
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")