class Board:
    def __init__(self):
        self.rows = {
            "red":    [2,3,4,5,6,7,8,9,10,11,12],
            "yellow": [2,3,4,5,6,7,8,9,10,11,12],
            "green":  [12,11,10,9,8,7,6,5,4,3,2],
            "blue":   [12,11,10,9,8,7,6,5,4,3,2]
        }

        self.marked = {
            "red": [],
            "yellow": [],
            "green": [],
            "blue": []
        }

    def mark(self, color, value):
        if value in self.rows[color]:
            self.marked[color].append(value)

    def display(self):
        for color in self.rows:
            line = color.upper() + ": "

            for number in self.rows[color]:
                if number in self.marked[color]:
                    line += f"[{number}] "
                else:
                    line += f" {number}  "

            print(line)