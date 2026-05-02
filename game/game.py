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
        self.current_player_index = 0
        self.rolls_this_turn = 0
        self.marked_this_turn = False  # wurde beim 1. Wurf schon was angekreuzt?
        self.turn_started = False
        self.penalty_this_turn = 0  # wie viele -5 in diesem Zug


        self.fullscreen = False

        # 🔥 WICHTIG
        self.request_exit = False

    def add_player(self, player):
        self.players.append(player)

    def update(self):
        pass

    def roll_dice(self):
        if self.rolls_this_turn >= 2:
            return
        if self.marked_this_turn and self.rolls_this_turn >= 1:
            return

        import random
        values = {
            "white1": random.randint(1, 6),
            "white2": random.randint(1, 6),
            "red":    random.randint(1, 6),
            "yellow": random.randint(1, 6),
            "green":  random.randint(1, 6),
            "blue":   random.randint(1, 6),
        }

        if self.roll is None:
            self.roll = {}

        self.roll = {"values": values}
        self.rolls_this_turn += 1

    def get_moves(self):
        if not self.roll:
            return None
        return get_moves(self.roll)
    
    def reset_game(self):
        print("🔄 Reset")

        self.roll = None
        self.current = 0

        # 🔥 SPIELER WIRKLICH RESETTEN
        self.players.clear()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)

        return screen

    def start_game(self):
        """Zufälligen Startspieler wählen"""
        self.current_player_index = random.randint(0, len(self.players) - 1)
        self.rolls_this_turn = 0
        self.marked_this_turn = False
        self.turn_started = True
        self.popup.open("turn_notify")  # ← kleiner Popup "X ist dran"

    @property
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.current_player_index]


    def on_mark(self):
        """Wird aufgerufen wenn ein Feld angekreuzt wird"""
        if self.rolls_this_turn == 1:
            self.marked_this_turn = True

    def next_turn(self):
        # Strafe: gewürfelt aber nichts markiert
        if self.rolls_this_turn > 0 and not self.marked_this_turn:
            cp = self.current_player
            if cp:
                cp.board.penalties += 1   # ← ein -5 Strafpunkt

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.rolls_this_turn = 0
        self.marked_this_turn = False
        self.penalty_this_turn = 0
        self.roll = {"values": None}
        self.popup.open("turn_notify")