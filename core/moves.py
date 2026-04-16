def get_moves(dice):
    moves = {
        "white": [],
        "red": [],
        "blue": [],
        "green": [],
        "yellow": []
    }

    # Weiß + Weiß
    moves["white"].append(dice["white1"] + dice["white2"])

    # Farb-Moves
    for color in ["red", "blue", "green", "yellow"]:
        moves[color].append(dice["white1"] + dice[color])
        moves[color].append(dice["white2"] + dice[color])

    return moves