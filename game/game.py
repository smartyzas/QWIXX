import random
from game.dice import Dice
from game.moves import get_moves
from ui.popup import Popup
import pygame



class Game:

    def __init__(self):
        self.players = []
        self.current = 0
        self.dice = Dice()
        self.roll = {"values": None}

    def add_player(self, player):
        self.players.append(player)

    def current_player(self):
        return self.players[self.current]

    def next_turn(self):
        self.current += 1
        if self.current >= len(self.players):
            self.current = 0

    def update(self):
        pass

    def handle_event(self, event):
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

    import pygame

    def toggle_fullscreen(self):

        screen = pygame.display.get_surface()

        if screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)