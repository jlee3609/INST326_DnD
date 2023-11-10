from Player import Player
from GameState import GameState
from argparse import ArgumentParser
import sys
import json


def main(item_path, location_path, num_players, end_location):
    #set up a round of DnD
    #initialize a bunch of players
    #pass players into the gamestate as a party
    party = {}
    for i in range(num_players):
        name = input("Please input player name: ")
        pclass = input("Please choose a class: ")
        character = Player(name, pclass)
        party[name] = character
        
    #do items
    with open(item_path, "r", encoding="utf-8") as f:
        for line in f:
            #csv (or json) with item name, price, effect, etc
            #I guessss we can regex it :vomit:
            #make a dict of Item objects with the item as the key and the number as the value
            pass
    
    #make game
    with open(location_path, "r", encoding="utf-8") as f:
        locations = json.load(f)
        
    game = GameState(items, locations, party)
    #game turns
    while game.location != end_location:
        game.new_turn()
    pass

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