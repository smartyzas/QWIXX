import random
import pygame
from game.dice import Dice
from game.moves import get_moves


# ═══════════════════════════════════════════
# ZUSTÄNDE (State Machine)
# ═══════════════════════════════════════════
# IDLE          → Warten auf Würfeln (rolls_this_turn == 0)
# PASSIVE       → Passive Spieler kreuzen Weiß+Weiß an (passive_phase == True)
# ACTIVE_CHOOSE → Würfler darf Farbe wählen ODER nochmal würfeln (active_player_phase, rolls_this_turn == 1)
# ACTIVE_COLOR  → Würfler darf NUR Farbe wählen, kein NOCHMAL mehr (rolls_this_turn == 2)
# ═══════════════════════════════════════════


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

        self.passive_queue   = []
        self.passive_index   = 0
        self.passive_phase   = False
        self.passive_timer   = 0
        self.PASSIVE_TIMEOUT = 20000

        self.active_player_phase  = False
        self.active_timer_running = False
        self.active_timer         = 0
        self.ACTIVE_TIMEOUT       = 30000

        self._auto_next_timer = None

    def add_player(self, player):
        self.players.append(player)

    # --------------------------------------------------
    def update(self):
        if self.passive_phase:
            if pygame.time.get_ticks() - self.passive_timer >= self.PASSIVE_TIMEOUT:
                self.passive_next()

        if self.active_timer_running:
            # ← Guard: nur feuern wenn wirklich noch ein Wurf aktiv ist
            if self.rolls_this_turn > 0 and self.roll and self.roll.get("values"):
                if pygame.time.get_ticks() - self.active_timer >= self.ACTIVE_TIMEOUT:
                    self.active_timer_running = False
                    self.active_player_phase  = False
                    self.next_turn()
            else:
                # Timer lief weiter obwohl Zug schon vorbei → stoppen
                self.active_timer_running = False

    # --------------------------------------------------
    def roll_dice(self):
        if self.rolls_this_turn >= 2:
            return
        # Würfler hat schon Phase 2 angekreuzt → kein 2. Wurf
        if self.marked_this_turn:
            return

        values = {
            "white1": random.randint(1, 6),
            "white2": random.randint(1, 6),
            "red":    random.randint(1, 6),
            "yellow": random.randint(1, 6),
            "green":  random.randint(1, 6),
            "blue":   random.randint(1, 6),
        }
        self.roll                 = {"values": values}
        self.rolls_this_turn     += 1
        self.active_player_phase  = False
        self.active_timer_running = False

        if len(self.players) > 1:
            self.start_passive_phase()
        else:
            self.active_player_phase = True
            white_sum = values["white1"] + values["white2"]
            self.popup.show_active_toast(self.current_player.name, white_sum)

    # --------------------------------------------------
    def _build_passive_queue(self):
        n   = len(self.players)
        idx = self.current_player_index
        ordered = [self.players[(idx + 1 + i) % n] for i in range(n - 1)]

        if self.rolls_this_turn == 2:
            # Nur die die beim 1. Wurf NICHT angekreuzt haben
            ordered = [p for p in ordered
                       if not getattr(p, 'marked_this_round', False)]

        return ordered

    # --------------------------------------------------
    def start_passive_phase(self):
        queue = self._build_passive_queue()

        if not queue:
            # Niemand übrig → direkt zur Würfler-Phase
            self._start_active_phase()
            return

        self.passive_queue = queue
        self.passive_index = 0
        self.passive_phase = True
        self.passive_timer = pygame.time.get_ticks()
        self._notify_passive_current()

    # --------------------------------------------------
    def _notify_passive_current(self):
        if self.passive_index < len(self.passive_queue):
            p         = self.passive_queue[self.passive_index]
            white_sum = self.roll["values"]["white1"] + self.roll["values"]["white2"]
            self.popup.show_passive_toast(p.name, white_sum)

    # --------------------------------------------------
    def passive_next(self):
        self.passive_index += 1
        self.passive_timer  = pygame.time.get_ticks()

        if self.passive_index >= len(self.passive_queue):
            self.passive_phase = False
            self.popup.hide_toast()
            self._start_active_phase()
        else:
            self._notify_passive_current()

    # --------------------------------------------------
    def _start_active_phase(self):
        # Guard: nur wenn wirklich ein Wurf existiert
        if not self.roll or not self.roll.get("values"):
            return

        self.active_player_phase  = True
        self.active_timer_running = True
        self.active_timer         = pygame.time.get_ticks()
        white_sum = self.roll["values"]["white1"] + self.roll["values"]["white2"]

        if self.rolls_this_turn == 1:
            self.popup.show_active_toast(self.current_player.name, white_sum)
        else:
            self.popup.show_active_color_only_toast(self.current_player.name, white_sum)

    # --------------------------------------------------
    def passive_current_player(self):
        if self.passive_phase and self.passive_index < len(self.passive_queue):
            return self.passive_queue[self.passive_index]
        return None

    # --------------------------------------------------
    @property
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.current_player_index]

    # --------------------------------------------------
    def on_mark(self, player=None):
        if player is None or player == self.current_player:
            self.marked_this_turn = True

    # --------------------------------------------------
    def next_turn(self):
        if self.rolls_this_turn > 0 and not self.marked_this_turn:
            self.current_player.board.penalties += 1

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        self.rolls_this_turn      = 0
        self.marked_this_turn     = False
        self.roll                 = {"values": None}
        self.passive_phase        = False
        self.passive_queue        = []
        self.passive_index        = 0
        self.active_player_phase  = False   # ← WICHTIG: VOR popup.open setzen
        self.active_timer_running = False
        self._auto_next_timer     = None

        for p in self.players:
            p.marked_this_round = False

        self.popup.hide_toast()
        self.popup.open("turn_notify")   # ← ruft show_turn_notify auf, NICHT _start_active_phase

    # --------------------------------------------------
    def get_allowed_marks(self):
        if not self.roll or not self.roll.get("values"):
            return set()
        v  = self.roll["values"]
        w1, w2 = v["white1"], v["white2"]
        white_sum = w1 + w2
        allowed = set()
        for color in ["red", "yellow", "green", "blue"]:
            allowed.add((color, white_sum))
            allowed.add((color, w1 + v[color]))
            allowed.add((color, w2 + v[color]))
        return allowed

    def get_allowed_marks_passive(self):
        if not self.roll or not self.roll.get("values"):
            return set()
        v         = self.roll["values"]
        white_sum = v["white1"] + v["white2"]
        allowed   = set()
        for color in ["red", "yellow", "green", "blue"]:
            allowed.add((color, white_sum))
        return allowed

    def get_moves(self):
        if not self.roll:
            return None
        return get_moves(self.roll)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
        return screen

    def start_game(self):
        self.current_player_index = random.randint(0, len(self.players) - 1)
        self.rolls_this_turn      = 0
        self.marked_this_turn     = False
        self.turn_started         = True
        self.active_player_phase  = False
        self.active_timer_running = False
        for p in self.players:
            p.marked_this_round = False
        self.popup.open("turn_notify")

    def reset_game(self):
        self.roll                 = {"values": None}
        self.current              = 0
        self.passive_phase        = False
        self.passive_queue        = []
        self.passive_index        = 0
        self.active_player_phase  = False
        self.active_timer_running = False
        self.players.clear()