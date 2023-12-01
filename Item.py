
class Item:
    """
    """
    def __init__(self, items, type, name):
        self.type = type
        self.name = name
        self.description = self.type[self.name]["description"]
        self.cost = self.type[self.name]["cost"]
        #dict within individ item's dict with listed changes to stats
        self.effects = {self.type[self.name]["effects"]} 
        self.quantity = self.type[self.name]["quantity"]
    def __str__(self):
        print(f"This is a {self.name}: {self.description}. Its effects are: ")
        
    def stats(self):
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")
            
