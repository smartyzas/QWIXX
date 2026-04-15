import random

class Dice:

    def __init__(self):
        self.dice_names = ["white1", "white2", "red", "blue", "green", "yellow"]
        self.values = {}

    def roll(self):
        self.values = {
            name: random.randint(1, 6)
            for name in self.dice_names
        }
        return self.values


my_dice = Dice()      # 1. Objekt erstellen
results = my_dice.roll()  # 2. Die Methode roll() aufrufen


print(results)



# ------------------------------------------------------------------
# Beispielzugriff:
# print(f"Summe Weiß: {results['white1'] + results['white2']}")
