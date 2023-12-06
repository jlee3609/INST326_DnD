import random
import json

class DnDRoller:
    """A dice roll simulation to determine outcomes, weapon damage, etc.
    Attributes:
    - dice (int): the type of die to roll (default is None) but can be 4, 6, 8, 10, 12, or 20.
    """
    def __init__(self, dice=None):
        """Initializes DnDRoller object.
        """
        self.dice = dice

    def roll_d20(self, advantage=False, disadvantage=False):
        """Simulates rolling a 20-sided die (d20).
        
        Side Effects:
            If advantage is True, the roll is determined by the maximum of two rolls.
            If disadvantage is True, the roll is determined by the minimum of two rolls.
        """
        roll_result = random.randint(1, 20)

        if advantage and disadvantage:
            raise ValueError("Can't have both. Try again!")
        elif advantage:
            result = max(roll_result, random.randint(1, 20))
        elif disadvantage:
            result = min(roll_result, random.randint(1, 20))

        return result

    def roll_sets(self, num_sides):
        """Simulates rolling a die with a specified number of sides.
        Side Effects:
            Raises a ValueError if the number of sides is less than 4
        """
        if num_sides < 4:
            raise ValueError("Number of sides on the die must be at least 4.")
        return random.randint(1, num_sides)
    
    def roll_with_set(self, num_sides):
        """Simulates rolling a die with a specified number of sides using roll_sets.
        Side Effects:
            Calls the roll_sets method to perform the die roll.
        """
        return self.roll_sets(num_sides)
    
    def roll_weapon(self, weapon_dice):
        """Simulates rolling the specified die associated with a weapon.
        Args:
            dice (list): The input list representing possible dice sets. It should contain at least one integer.
            weapon_dice (dict): A dictionary representing the weapon's attributes, including 'damage_attr'.
        Side Effects:
            Prints the result of the simulated weapon roll.
        Raises:
            ValueError: If 'damage_attr' is not present in the weapon_dice.
        """
        print("Rolling weapon...")
        if "damage_attr" in weapon_dice:
            num_sides = weapon_dice["damage_attr"]
            result = self.roll_with_set(num_sides)
            print(f"You rolled a d{num_sides} for damage and got: {result}")
        else:
            raise ValueError("Pick a real weapon, why don'tcha?")
            
if __name__ == "__main__":
    roller = DnDRoller()

    while True:
        print("Choose an option:")
        print("1. Roll a d20.")
        print("2. Roll die associated with weapon.")
        print("3. Roll a custom die.")
        print("4. Quit.")

        choice = input("Enter your choice: ")
        
        p_items_json = "items.json"
        with open(p_items_json, 'r') as file:
            items_json = json.load(file)

        if choice == '1':
            advantage = input("Do you have advantage? (y/n): ").lower() == 'y'
            if advantage == True:
                result = roller.roll_d20(advantage=advantage)
                print(f"You rolled a d20 and got: {result}")
            elif advantage == False:
                disadvantage = input("Do you have disadvantage? (y/n): ").lower() == 'y'
                result = roller.roll_d20(disadvantage=disadvantage)
                print(f"You rolled a d20 and got: {result}")
        elif choice == '2':
            weapon_choice = input("Enter the name of the weapon: ").strip()
            
            weapon_data = items_json['weapon'].get(weapon_choice)

            if weapon_data and 'damage_attr' in weapon_data:
                num_sides = weapon_data['damage_attr']
                result = roller.roll_with_set(num_sides)
                print(f"You rolled the d{num_sides} for damage and got: {result}. Add this to existing damage.")
            else:
                print("Invalid weapon choice.")
                
        elif choice == '3':
            num_sides = int(input("Enter the number of sides for the higher die: "))
            result = roller.roll_with_set(num_sides)
            print(f"You rolled a d{num_sides} and got: {result}")
        elif choice == '4':
            print("Farewell...")
            break
        else:
            print("Choose from the above choices. No funny business.")
