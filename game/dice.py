import random

class Dice:
    def roll(self):
        return {
            "white1": random.randint(1, 6),
            "white2": random.randint(1, 6),
            "red": random.randint(1, 6),
            "yellow": random.randint(1, 6),
            "green": random.randint(1, 6),
            "blue": random.randint(1, 6),
        }