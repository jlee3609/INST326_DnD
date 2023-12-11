
class Item:
    """ Class of an item that a player can buy, own, or use.
    Author: Ariel Hong
    
    Attributes:
        items (list of dicts of str:(dict of str:vals): All the items in the game.
            Each key is the item type; each value is a dict containing the 
            description, cost, effects (another dict of str:int), and quantity 
            of each item.
        type (str): the type of Item, either "potion", "armor", or "weapon".
        name (str): the name of an Item
        description (str): the Item's description.
        cost (int): the cost to purchase Item.
        effects (dict of str:int): the stat changes. Each key is the Player's stats;
            each value is an int of the changes each object makes to the Player's stats
        quantity (int): how many of the item there are in existence.
        damage (int): the damage an item does when used in the attack method
    """
    def __init__(self, items, type, name):
        """ Initializes instance of an Item.
        Author: Nicole Tran, Ariel Hong
        
        Args:
            items (list of dicts of str:(dict of str:vals): All the items in the
                game. Each key is the item type; each value is a dict containing
                the description, cost, effects (another dict of str:int), and 
                quantity of each item.
            type (str): the type of Item, either "potion", "armor", or "weapon".
            name (str): the name of an Item.
            
        Side effects:
            Sets `items`, `type`, `name`, `description`, `cost`, `effects`, `quantity` and
            `damage` attributes.
        """
        self.items = items.copy()
        self.type = type
        self.name = name
        self.description = self.items[self.type][self.name]["description"]
        self.cost = self.items[self.type][self.name]["cost"]
        #dict within individ item's dict with listed changes to stats
        self.effects = self.items[self.type][self.name]["effects"]
        self.quantity = self.items[self.type][self.name]["quantity"]
        self.damage = self.items[self.type][self.name]["damage"]
        
    def __str__(self):
        """ Informal string representation of an item: Includes name and description
        Author: Nicole Tran
        Technique: Magic methods other than __init__
        
        Returns:
            f-string: formal string representation of an item.
        """
        return f"This is a {self.name}: {self.description}"
        
    def stats(self):
        """ More detailed description of an item, lists what effects it has to stats
        Author: Nicole Tran
        
        Side effects:
            Prints to terminal
        """
        for effect in self.effects:
            print(f"Adds {self.effects[effect]} to {effect}")
            
