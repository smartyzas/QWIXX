# game/player.py

from game.board import Board


class Player:

    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.penalty = 0

    def add_penalty(self, value=5):
        self.penalty -= value