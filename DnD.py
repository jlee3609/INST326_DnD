from Player import Player
from GameState import GameState
from argparse import ArgumentParser
import sys


def main(item_path, location_path, num_players):
    #set up a round of DnD
    #initialize a bunch of players
    #pass players into the gamestate as a party
    
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