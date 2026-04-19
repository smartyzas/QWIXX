def get_moves(roll):

    white = roll["white1"] + roll["white2"]

    return {
        "white": [white],
        "red": [roll["white1"] + roll["red"], roll["white2"] + roll["red"]],
        "yellow": [roll["white1"] + roll["yellow"], roll["white2"] + roll["yellow"]],
        "green": [roll["white1"] + roll["green"], roll["white2"] + roll["green"]],
        "blue": [roll["white1"] + roll["blue"], roll["white2"] + roll["blue"]],
    }