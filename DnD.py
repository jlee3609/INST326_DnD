from Player import Player
from Item import Item
from GameState import GameState
from argparse import ArgumentParser
import sys
import json
import re


def main(item_path, location_path, num_players):
    """Sets up a round of Dungeons and Dragons. Initializes players, pass those
    players into the GameState as a party. Loads items, loads locations, and sets
    up for when players reach the final location.
    Args:
        location_path():
        num_players(int): number of players to be added to party
    """
    #set up a round of DnD
    #initialize a bunch of players
    #pass players into the gamestate as a party
    party = {}
    for i in range(num_players):
        classes = ["Mage", "Healer", "Tank", "Assassin", "Berserker"]
        name = input("Please input player name: ")
        print("The possible classes are: Mage, Healer, Tank, Assassin, Berserker")
        pclass = input("Please choose a class: ")
        while not re.match(r'^[Mm]age|[Hh]ealer|[Tt]ank|[Aa]ssassin|[Bb]erserker$', pclass):
            if pclass not in classes:
                pclass = input("Please choose a valid class: ")
        character = Player(name, pclass, "Player")
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
        
        list_items = potions+armors+weapons
        items = {}
        for item in list_items:
            items[item.name] = item
    
    #make game
    #load locations and set final location
    with open(location_path, "r", encoding="utf-8") as f:
        locations = json.load(f)
        end_location = locations["final_location"]["final"]
        
    game = GameState(items, locations, party, end_location)
    #game turns
    while (game.curr_location != end_location) and len(game.party)!=0:
        game.new_turn()

    #end the game somehow?
    #print that its the endgame locaiton, make a boss npc, and do battle
    if game.curr_location == end_location:
        print(f"Your party has reached {end_location}! Please prepare to meet the final boss.")
        game.new_turn()
        x=input("\nNow entering Boss Battle! Prepare yourselves.\n")
        game.battle("neutral", boss=True)
    
    if len(game.party) == 0:
        print("Your party has lost, please play again soon!")
    else:
        print("Congratulations on beating the Adventures of INST326!")

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
    main(args.item_path, args.location_path, args.num_players)