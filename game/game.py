import random
import pygame
from game.dice import Dice
from game.moves import get_moves

class Game:

    def __init__(self):
        self.players = []
        self.current = 0
        self.dice = Dice()
        self.roll = {"values": None}

        self.fullscreen = False

        # 🔥 WICHTIG
        self.request_exit = False

    def add_player(self, player):
        self.players.append(player)

    def current_player(self):
        return self.players[self.current]

    def next_turn(self):
        self.current = (self.current + 1) % len(self.players)

    def update(self):
        pass

    def roll_dice(self):
        values = self.dice.roll()
        self.roll["values"] = values

    def get_moves(self):
        if not self.roll:
            return None
        return get_moves(self.roll)

    def reset_game(self):
        print("🔄 Reset")
        self.roll = {"values": None}

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)

        return screen