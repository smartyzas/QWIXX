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
        self.marked_this_turn = False
        self.turn_started = False
        self.penalty_this_turn = 0
        self.fullscreen = False
        self.request_exit = False
        self.roll_1 = None
        self.roll_2 = None

        self.passive_queue = []
        self.passive_index = 0
        self.passive_phase = False
        self.passive_timer = 0
        self.PASSIVE_TIMEOUT = 15000
        self.ACTIVE_TIMEOUT  = 20000
        self.active_player_phase = False
        self.active_timer_running = False
        self.active_timer         = 0
        self._auto_next_timer = None


    def add_player(self, player):
        self.players.append(player)

    def update(self):
        if self.passive_phase:
            if pygame.time.get_ticks() - self.passive_timer >= self.PASSIVE_TIMEOUT:
                self.passive_next()

        if self.active_timer_running:
            if pygame.time.get_ticks() - self.active_timer >= self.ACTIVE_TIMEOUT:
                self.active_timer_running = False
                self.active_player_phase  = False
                self.next_turn()

        # NEU: Zug automatisch beenden nach 2s wenn marked oder 2x gewürfelt
        if (self.marked_this_turn or self.rolls_this_turn >= 2) and not self.passive_phase and not self.active_timer_running:
            if self._auto_next_timer is None:
                self._auto_next_timer = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self._auto_next_timer >= 1000:  # 1 Sekunde
                self._auto_next_timer = None
                self.next_turn()
        else:
            self._auto_next_timer = None

    def roll_dice(self):
        self.active_timer_running = False
        if self.rolls_this_turn >= 2:
            return
        if self.marked_this_turn and self.rolls_this_turn >= 1:
            return

        values = {
            "white1": random.randint(1, 6),
            "white2": random.randint(1, 6),
            "red":    random.randint(1, 6),
            "yellow": random.randint(1, 6),
            "green":  random.randint(1, 6),
            "blue":   random.randint(1, 6),
        }
        self.roll = {"values": values}
        self.rolls_this_turn += 1
        self.active_player_phase = True

        self.start_passive_phase()

        if self.rolls_this_turn == 1:
            self.roll_1 = values
        elif self.rolls_this_turn == 2:
            self.roll_2 = values

        if len(self.players) > 1:
            self.start_passive_phase()
        else:
            white_sum = values["white1"] + values["white2"]
            self.popup.show_roll_toast(white_sum)
                
    def start_passive_phase(self):
        if self.rolls_this_turn == 1:
            # 1. Wurf: alle anderen Spieler
            others = [p for p in self.players if p != self.current_player]
        else:
            # 2. Wurf: nur die die beim 1. Wurf NICHT angekreuzt haben
            others = [p for p in self.players
                    if p != self.current_player
                    and not getattr(p, 'marked_this_round', False)]

        if not others:
            # Alle haben schon angekreuzt → Würfler direkt dran
            self.passive_phase        = False
            self.active_player_phase  = True
            self.active_timer_running = True
            self.active_timer         = pygame.time.get_ticks()
            self.popup.show_wuerfler_toast(self.current_player.name)
            return

        self.passive_queue = others
        self.passive_index = 0
        self.passive_phase = True
        self.passive_timer = pygame.time.get_ticks()
        self._notify_passive_current()

    def _notify_passive_current(self):
        if self.passive_index < len(self.passive_queue):
            p = self.passive_queue[self.passive_index]
            white_sum = self.roll["values"]["white1"] + self.roll["values"]["white2"]
            self.popup.show_passive_toast(p.name, white_sum)

    def passive_next(self):
        self.passive_index += 1
        self.passive_timer = pygame.time.get_ticks()
        if self.passive_index >= len(self.passive_queue):
            self.passive_phase        = False
            self.active_player_phase  = True
            self.active_timer_running = True
            self.active_timer         = pygame.time.get_ticks()
            self.popup.show_wuerfler_toast(self.current_player.name)
        else:
            self._notify_passive_current()

    def _notify_active_player(self):
        white_sum = self.roll["values"]["white1"] + self.roll["values"]["white2"]
        self.popup.show_active_toast(self.current_player.name, white_sum)
        self.active_player_phase = True

    def passive_current_player(self):
        if self.passive_phase and self.passive_index < len(self.passive_queue):
            return self.passive_queue[self.passive_index]
        return None

    def get_moves(self):
        if not self.roll:
            return None
        return get_moves(self.roll)

    def reset_game(self):
        self.roll = None
        self.current = 0
        self.passive_phase = False
        self.passive_queue = []
        self.passive_index = 0
        self.active_player_phase = False
        self.players.clear()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
        return screen

    def start_game(self):
        self.current_player_index = random.randint(0, len(self.players) - 1)
        self.rolls_this_turn = 0
        self.marked_this_turn = False
        self.turn_started = True
        self.active_player_phase = False
        for p in self.players:
            p.marked_this_round = False
        self.popup.open("turn_notify")

    @property
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.current_player_index]
    def on_mark(self, player=None):
        if player is None or player == self.current_player:
            self.marked_this_turn = True

    def next_turn(self):
        for p in self.players:
            p.marked_this_round = False
        if self.rolls_this_turn > 0 and not self.marked_this_turn:
            self.current_player.board.penalties += 1
            self.roll_1 = None
            self.roll_2 = None

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.rolls_this_turn = 0
        self.marked_this_turn = False
        self.roll = {"values": None}
        self.passive_phase = False
        self.passive_queue = []
        self.passive_index = 0
        self.active_player_phase = False
        self.active_timer_running = False   # ← NEU
        self.active_timer         = 0

        for p in self.players:
            p.marked_this_round = False

        self.popup.open("turn_notify")

    def get_allowed_marks(self):
        if not self.roll or not self.roll.get("values"):
            return set()
        v = self.roll["values"]
        w1, w2 = v["white1"], v["white2"]
        white_sum = w1 + w2
        allowed = set()
        for color in ["red", "yellow", "green", "blue"]:
            allowed.add((color, white_sum))
            allowed.add((color, w1 + v[color]))
            allowed.add((color, w2 + v[color]))
        return allowed

    def get_allowed_marks_passive(self):
        allowed = set()
        for roll_values in [self.roll_1, self.roll_2]:
            if not roll_values:
                continue
            white_sum = roll_values["white1"] + roll_values["white2"]
            for color in ["red", "yellow", "green", "blue"]:
                allowed.add((color, white_sum))
        return allowed