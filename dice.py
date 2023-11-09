import random

class DnDRoller:
    def __init__(self, dice):
        self.dice = dice

    #for d20 dice
    def roll_d20():
        return random.randint(1, 20)

    # dice sets 4, 6, 8, 10, and 12
    def roll_sets(num_sides):
        if num_sides < 2:
            raise ValueError("Number of sides on the die must be at least 2.")
        return random.randint(1, num_sides)

    def roll_with_set():
        pass

if __name__ == "__main__":
    roller = DnD20Roller()
    
    while True:
        print("Choose an option:")
        print("1. Roll a d20")
        print("2. Roll a custom die")
        print("3. Roll custom dice with modifier")
        print("4. Quit")
        
        choice = input("Enter your choice: ")
    # continue
