import random

class DnDRoller:
    def __init__(self, dice=None):
        self.dice = dice

    def roll_d20(self, advantage=False, disadvantage=False):
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
        if num_sides < 4:
            raise ValueError("Number of sides on the die must be at least 4.")
        return random.randint(1, num_sides)

    def roll_with_set(self, num_sides):
        return self.roll_sets(num_sides)

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
