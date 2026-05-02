class Board:
    def __init__(self):
        self.rows = {
            "red": list(range(2, 13)),
            "yellow": list(range(2, 13)),
            "green": list(range(12, 1, -1)),
            "blue": list(range(12, 1, -1))
        }

        self.marked = {
            "red": [],
            "yellow": [],
            "green": [],
            "blue": []
        }

        self.locked = {
            "red": False,
            "yellow": False,
            "green": False,
            "blue": False
        }
        self.penalties = 0

    def can_mark(self, color, value):
        if self.locked[color]:
            return False

        if value in self.marked[color]:
            return False

        if not self.marked[color]:
            return True

        last = self.marked[color][-1]

        if color in ["red", "yellow"]:
            return value > last

        return value < last

    def mark(self, color, value):
        if not self.can_mark(color, value):
            return False

        self.marked[color].append(value)
        return True
    
    def lock_row(self, color):
        self.locked[color] = True

    def get_score(self, color):
        crosses = len(self.marked[color])
        if self.locked[color]:
            crosses += 1
        # Dreieckszahl: n*(n+1)/2
        return crosses * (crosses + 1) // 2

    def get_total_score(self):
        total = sum(self.get_score(color) for color in ["red", "yellow", "green", "blue"])
        return total - (self.penalties * 5)