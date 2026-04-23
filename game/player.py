# game/player.py

from game.board import Board


class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = {
            "red": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0
        }
        
    def add_penalty(self, value=5):
        self.penalty -= value

