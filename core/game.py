from dice import Dice
from moves import get_moves


def moves():
    dice = Dice()

    roll = dice.roll()
    print("Wurf:", roll)

    moves = get_moves(roll)
    print("Moves:", moves)

moves()