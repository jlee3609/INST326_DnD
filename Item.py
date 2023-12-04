
class Item:
    """
    
    Attributes:
        items ():
        type ():
        name ():
        description ():
        cost ():
        effects ():
        quantity ():
    """
    def __init__(self, items, type, name):
        """ Initializes instance of an Item.
        
        Args:
            items ():
            type ():
            name ():
            
        Side effects:
            Sets `items`, `type`, `name`, `description`, `cost`, `effects`, and
            `quantity` attributes.
        """
        self.items = items.copy()
        self.type = type
        self.name = name
        self.description = self.items[self.type][self.name]["description"]
        self.cost = self.items[self.type][self.name]["cost"]
        #dict within individ item's dict with listed changes to stats
        self.effects = self.items[self.type][self.name]["effects"]
        self.quantity = self.items[self.type][self.name]["quantity"]
        
    def __str__(self):
        """
        """
        return f"This is a {self.name}: {self.description} Its effects are: {self.effects}"
        
    def stats(self):
        """
        """
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")
            
