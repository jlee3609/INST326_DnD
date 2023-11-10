
class Item:
    """
    """
    def __init__(self, item, name):
        self.type = item[type]
        self.name = name
        self.description = self.type[self.name]["description"]
        
        #dict within individ item's dict with listed changes to stats
        self.effects = {self.type[self.name]["effects"]} 
        self.quantity = self.type[self.name]["quantity"]
    def stats(self):
        print(f"This is a {self.name}: {self.description}. Its effects are: ")
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")
            
