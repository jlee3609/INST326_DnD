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
            raise ValueError("Cannot have both advantage and disadvantage.")
        elif advantage:
            result = max(roll_result, random.randint(1, 20))
        elif disadvantage:
            result = min(roll_result, random.randint(1, 20))

        return result

    # dice sets 4, 6, 8, 10, and 12
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

    def roll_weapon(self, dice, advantage=False):
        """Simulates rolling the dice associated with a weapon in json file.

        Args:
            dice (list): The input list representing possible dice sets. It should contain at least one integer.
            advantage (boolean): A flag to indicate whether advantage is applied. Defaults to False.
        """
        if advantage:
            num_sides = max(dice[1], dice[0])  #the second, the higher die
        else:
            num_sides = min(dice[0], dice[1])  #the first element, the lower die

        result = self.roll_sets(num_sides)
        return result

if __name__ == "__main__":
    roller = DnDRoller()

    while True:
        print("Choose an option:")
        print("1. Roll a d20")
        print("2. Roll lower die associated with weapon")
        print("3. Roll higher die associated with weapon")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            advantage = input("Do you have advantage? (y/n): ").lower() == 'y'
            disadvantage = input("Do you have disadvantage? (y/n): ").lower() == 'y'
            result = roller.roll_d20(advantage=advantage, disadvantage=disadvantage)
            print(f"You rolled a d20 and got: {result}")
        elif choice == '2':
            num_sides = int(input("Enter the number of sides for the lower die: "))
            result = roller.roll_with_set(num_sides)
            print(f"You rolled a d{num_sides} and got: {result}")
        elif choice == '3':
            num_sides = int(input("Enter the number of sides for the higher die: "))
            result = roller.roll_with_set(num_sides)
            print(f"You rolled a d{num_sides} and got: {result}")
        elif choice == '4':
            break
        else:
            print("Choose from the above choices. No funny business.")
