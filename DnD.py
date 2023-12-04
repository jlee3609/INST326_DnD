from Player import Player
from Item import Item
from GameState import GameState
from argparse import ArgumentParser
import sys
import json


def main(item_path, location_path, num_players):
    #set up a round of DnD
    #initialize a bunch of players
    #pass players into the gamestate as a party
    party = {}
    for i in range(num_players):
        name = input("Please input player name: ")
        print("The possible classes are: Mage, Healer, Tank, Assassin, Berserker")
        pclass = input("Please choose a class: ")
        character = Player(name, pclass, 20)
        party[name] = character
        
    #load items
    with open(item_path, "r", encoding="utf-8") as f:
        items = json.load(f)
        potion_names = list(items["potion"])
        armor_names = list(items["armor"])
        weapon_names = list(items["weapon"])
        potions = []
        armors = []
        weapons = []
        for potion in potion_names:
            potions.append(Item(items, "potion", potion))
        for armor in armor_names:
            armors.append(Item(items, "armor", armor)) 
        for weapon in weapon_names:
            weapons.append(Item(items, "weapon", weapon)) 
        
        items = potions+armors+weapons 
    
    #make game
    #load locations and set final location
    with open(location_path, "r", encoding="utf-8") as f:
        locations = json.load(f)
        end_location = locations["final_location"]["final"]
        
    game = GameState(items, locations, party)
    #game turns
    while game.curr_location != end_location:
        game.new_turn()
    #end the game somehow?
    #print that its the endgame locaiton, make a boss npc, and do battle
    print(f"Your party has reached {end_location}! Please prepare to meet the final boss.")
    game.battle("neutral", boss=True)

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect two mandatory arguments:
        - item_path: a path to a file containing the items
        - location_path: a path to a json containing the locations
        - num_players: the number of players
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("item_path", help="path to word list text file")
    parser.add_argument("location_path", help="path to locations json")
    parser.add_argument("num_players", type=int, help="the number of players")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(args)
    main(args.item_path, args.location_path, args.num_players)