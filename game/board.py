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