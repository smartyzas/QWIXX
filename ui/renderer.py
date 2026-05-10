import os
import pygame
from config import *

class Renderer:

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.font_big = pygame.font.Font("assets/caveat-bold.ttf", 40)
        self.font_small = pygame.font.Font("assets/caveat-bold.ttf", 20)
        self.font_logo = pygame.font.Font("assets/caveat-bold.ttf", 80)
        self.font_logo_small = pygame.font.Font("assets/caveat-bold.ttf", 32)
        self.font_wuerfel_button = pygame.font.Font("assets/caveat-bold.ttf", 32)
        self.font_wuerfel_zahl = pygame.font.SysFont("arial", 40, bold=True)

        # buttons
        self.btn_exit = pygame.Rect(0, 0, 0, 0)
        self.btn_reset = pygame.Rect(0, 0, 0, 0)
        self.btn_roll = pygame.Rect(0, 0, 0, 0)
        self.btn_roll = pygame.Rect(0, 0, 0, 0)
        self.cell_rects = {}   # ← NEU, nach self.btn_roll
        self.confirm_reroll = False

        # icons
        self.icon_exit = pygame.image.load("assets/exit_button.png").convert_alpha()
        self.icon_reset = pygame.image.load("assets/reset_button.png").convert_alpha()
        self.icon_lock_field = pygame.image.load("assets/lock.png").convert_alpha()

        self.colors = {
        "exit": (180, 70, 70),        # 🔴 weiches dunkleres Rot (wie roter Würfel)
        "reset": (120, 120, 120),     # ⚪ Grau bleibt gleich
        "roll": (85, 95, 90),         # (optional unverändert)
        }
        
        pygame.display.set_caption("QWIXX")

        # 🔥 HIER EINBAUEN
        icon_path = os.path.join("assets", "qwixx_window_icon.png")

        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(icon)
        else:
            print("⚠️ Icon fehlt:", icon_path)


    # ----------------------------
    def draw_text(self, text, x, y, center=False):
        img = self.font_logo.render(text, True, (220, 220, 220))
        rect = img.get_rect()

        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(img, rect)

    # ----------------------------
    def draw_button(self, rect, text, key, font=None):
        color = self.colors.get(key, (100, 100, 100))

        shadow = rect.move(2, 2)
        pygame.draw.rect(self.screen, (0, 0, 0, 80), shadow, border_radius=12)
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255, 35), rect, 1, border_radius=12)

        f = font if font else self.font_small  # ← NEU

        txt = f.render(text, True, (255, 255, 255))
        txt_shadow = f.render(text, True, (0, 0, 0))

        txt_rect = txt.get_rect(center=rect.center)
        self.screen.blit(txt_shadow, (txt_rect.x + 1, txt_rect.y + 1))
        self.screen.blit(txt, txt_rect)

    # ----------------------------
    def draw_icon_button(self, rect, image, key):

        color = self.colors.get(key, (80, 80, 80))

        # shadow
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, 80),
            (0, 0, rect.width, rect.height),
            border_radius=14
        )
        self.screen.blit(shadow, (rect.x + 2, rect.y + 2))

        # main
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        pygame.draw.rect(
            surface,
            color,
            (0, 0, rect.width, rect.height),
            border_radius=14
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255, 35),
            (0, 0, rect.width, rect.height),
            width=1,
            border_radius=14
        )

        self.screen.blit(surface, rect.topleft)

        # icon centered (smooth scaling)
        padding = 10
        icon_size = rect.width - padding * 2

        img = pygame.transform.smoothscale(image, (icon_size, icon_size))
        img_rect = img.get_rect(center=rect.center)

        self.screen.blit(img, img_rect)

    def draw_dice(self, x, y, size, value, color):

        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        rect = pygame.Rect(0, 0, size, size)

        # shadow (weich)
        shadow = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), rect, border_radius=18)
        self.screen.blit(shadow, (x+3, y+3))

        # main dice
        pygame.draw.rect(surface, color, rect, border_radius=18)

        # soft border (wichtig!)
        pygame.draw.rect(surface, (255, 255, 255, 60), rect, width=2, border_radius=18)

        self.screen.blit(surface, (x, y))

        if value is not None:
            txt = self.font_wuerfel_zahl.render(
                str(value),
                True,
                (20, 20, 20) if color == WHITE else (255, 255, 255)
            )
            txt_rect = txt.get_rect(center=(x + size//2, y + size//2))
            self.screen.blit(txt, txt_rect)

        # ----------------------------

    def draw_board(self, x, y, scale=1.0, player=None, allowed=None):

        row_h = int(38 * scale)
        cell_w = int(46 * scale)
        gap = 5

        colors = [
            (200, 70, 70),
            (230, 210, 60),
            (70, 170, 70),
            (70, 110, 220)
        ]
        row_names = ["red", "yellow", "green", "blue"]
        LOCKED_COLOR = (85, 95, 90)
        LOCK_READY   = (190, 160, 50)

        rows = [
            list(range(2, 13)),
            list(range(2, 13)),
            list(range(12, 1, -1)),
            list(range(12, 1, -1))
        ]

        for r in range(4):
            row_y = y + r * (row_h + gap)
            row_color = row_names[r]

            is_locked = player and player.board.locked[row_color]
            can_lock  = player and len(player.board.marked[row_color]) >= 5 and not is_locked

            for i, num in enumerate(rows[r]):
                rect = pygame.Rect(
                    x + i * (cell_w + gap),
                    row_y,
                    cell_w,
                    row_h
                )

                if is_locked:
                    cell_color = LOCKED_COLOR
                else:
                    cell_color = colors[r]

                pygame.draw.rect(self.screen, cell_color, rect, border_radius=5)

                if not is_locked and allowed is not None and (row_color, num) in allowed:
                    glow = rect.inflate(4, 4)
                    glow_surf = pygame.Surface((glow.width, glow.height), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (240, 235, 210, 80), (0, 0, glow.width, glow.height), border_radius=7)
                    self.screen.blit(glow_surf, glow.topleft)
                    pygame.draw.rect(self.screen, (240, 235, 210), rect, 2, border_radius=5)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=5)

                if player and num in player.board.marked[row_color]:
                    x_txt = self.font_small.render("X", True, (255, 255, 255) if is_locked else BLACK)
                    self.screen.blit(x_txt, x_txt.get_rect(center=rect.center))
                else:
                    txt_color = (120, 120, 120) if is_locked else BLACK
                    txt = self.font_small.render(str(num), True, txt_color)
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

                if player:
                    self.cell_rects[(id(player), row_color, num)] = rect

            lock_rect = pygame.Rect(
                x + 11 * (cell_w + gap) + 8,
                row_y,
                row_h,
                row_h
            )

            if is_locked:
                lock_bg = LOCKED_COLOR
            elif can_lock:
                lock_bg = LOCK_READY
            else:
                lock_bg = (128, 110, 108)

            pygame.draw.rect(self.screen, lock_bg, lock_rect, border_radius=5)
            pygame.draw.rect(self.screen, WHITE, lock_rect, 1, border_radius=5)

            padding = 4
            icon_size = lock_rect.width - padding * 2
            lock_img = pygame.transform.smoothscale(self.icon_lock_field, (icon_size, icon_size))
            self.screen.blit(lock_img, lock_img.get_rect(center=lock_rect.center))

            if player:
                self.cell_rects[(id(player), row_color, "lock")] = lock_rect
                
    def draw_player_name(self, name, char_x, base_y, color=(220, 220, 220)):
        if len(name) <= 9:
            txt = self.font_small.render(name, True, color)
            self.screen.blit(txt, txt.get_rect(center=(char_x, base_y)))
            return txt.get_rect(center=(char_x, base_y))
        else:
            line1 = name[:9] + "-"
            line2 = name[9:]
            line_h = self.font_small.size("A")[1]
            gap = 3
            txt1 = self.font_small.render(line1, True, color)
            txt2 = self.font_small.render(line2, True, color)
            total_h = line_h * 2 + gap
            y1 = base_y - total_h // 2 + line_h // 2
            y2 = y1 + line_h + gap
            self.screen.blit(txt1, txt1.get_rect(center=(char_x, y1)))
            self.screen.blit(txt2, txt2.get_rect(center=(char_x, y2)))
            return txt1.get_rect(center=(char_x, y1))
        
 #-----------------------------------------
    def draw(self):

        if self.game.popup.active and self.game.popup.mode != "turn_notify":
            return
      
        width, height = self.screen.get_size()
        self.cell_rects = {}

        ui_scale = min(width / 1920, height / 1080)   # ← Basis jetzt 1920x1080
        scale = ui_scale
        scale = max(0.5, scale)

        base_scale = ui_scale
        base_scale = max(0.5, base_scale)

        self.font_logo           = pygame.font.Font("assets/caveat-bold.ttf", max(20, int(80  * ui_scale)))
        self.font_logo_small     = pygame.font.Font("assets/caveat-bold.ttf", max(14, int(32  * ui_scale)))
        self.font_wuerfel_button = pygame.font.Font("assets/caveat-bold.ttf", max(14, int(32  * ui_scale)))
        self.font_wuerfel_zahl   = pygame.font.SysFont("arial", max(14, int(40 * ui_scale)), bold=True)
        self.font_small          = pygame.font.Font("assets/caveat-bold.ttf", max(10, int(20 * ui_scale)))

        btn_size = int(36 * scale)
        btn_roll_w = int(180 * scale)
        btn_roll_h = int(45 * scale)

        # QWIXX Titel 
        txt_qwixx = self.font_logo.render("QWIXX", True, (220, 220, 220))
        rect_qwixx = txt_qwixx.get_rect(center=(width * 0.87, height * 0.45))
        self.screen.blit(txt_qwixx, rect_qwixx)

        # LENI EDITION darunter
        txt = self.font_logo_small.render("Leni Edition", True, (220, 220, 220))
        rect = txt.get_rect(center=(width * 0.87, height * 0.50))
        self.screen.blit(txt, rect)

        base_size = 65
        dice_size = int(base_size * scale * 0.9)

        # =====================================================
        # SPIELER POSITIONEN
        # =====================================================

        count = len(self.game.players)

        w, h = self.screen.get_size()

        left_x = int(w * 0.03)
        right_x = int(w * 0.80)

        top     = int(h * 0.10)
        spacing = int(h * 0.30)   # ← 360px auf FHD ≈ h*0.33, passt sich an

        offset = int(h * 0.055)   # ← 50px auf FHD, skaliert auf allen Auflösungen

        if count == 2:
            positions = [
                (left_x, int(h * 0.20) + offset),
                (left_x, int(h * 0.55) + offset),
            ]
        elif count == 3:
            positions = [
                (left_x, top + offset),
                (left_x, top + spacing + offset),
                (left_x, top + spacing * 2 + offset),
            ]
        elif count == 4:
            positions = [
                (left_x, top + offset),
                (left_x, top + spacing + offset),
                (left_x, top + spacing * 2 + offset),
                (right_x, top + offset),
            ]
        elif count == 5:
            positions = [
                (left_x, top + offset),
                (left_x, top + spacing + offset),
                (left_x, top + spacing * 2 + offset),
                (right_x, top + offset),
                (right_x, top + spacing * 2 + offset),
            ]

        # =====================================================
        # SPIELER ZEICHNEN
        # =====================================================

        player_scale = min(width / 1400, height / 900)
        player_scale = max(0.72, min(player_scale, 1.45))

        is_small_window = width < 1000 or height < 700

        body_r = int(32 * player_scale)
        head_r = int(24 * player_scale)
        score_r = int(22 * player_scale)

        font_size = int(28 * player_scale)
        self.font_small = pygame.font.SysFont("assets/caveat-bold.ttf", font_size, bold=True)

        for i, player in enumerate(self.game.players):
            if i >= len(positions):
                continue

            x, y = positions[i]
            right_side = x > width / 2

            # ← HIER, einmal pro Spieler
            allowed = self.game.get_allowed_marks() if self.game.rolls_this_turn > 0 else None
            # =================================================
            # LINKS
            # =================================================
            if not right_side:

                char_x = x + body_r - 10
                body_y = y + body_r
                head_y = y - int(15 * player_scale)

                pygame.draw.circle(self.screen, player.color, (char_x, body_y - 10), body_r)
                pygame.draw.circle(self.screen, player.color, (char_x, head_y - 10), head_r)

                is_active = (player == self.game.current_player)
                is_passive_turn = (
                    self.game.passive_phase and
                    player == self.game.passive_current_player()
                )

                if is_active:
                    name_color = (255, 215, 0)       # Gelb — würfelt gerade
                elif is_passive_turn:
                    name_color = (100, 220, 130)     # Grün — darf jetzt W+W ankreuzen
                else:
                    name_color = (220, 220, 220)     # Weiß — wartet

                self.draw_player_name(player.name, char_x, y - int(58 * player_scale) - 15, color=name_color)

                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]
                row_names    = [None, "red", "yellow", "green", "blue"]
                start_x      = x + int(245 * player_scale)    # ← DAS FEHLTE

                for j, sc in enumerate(score_colors):
                    cx = start_x + j * int(44 * player_scale)
                    cy = y - int(72 * player_scale)
                    pygame.draw.circle(self.screen, sc, (cx, cy), score_r)

                    if j == 0:
                        if player.board.penalties > 0:
                            penalty_txt = f"-{player.board.penalties * 5}"
                            pts_txt = self.font_small.render(penalty_txt, True, (120, 120, 120))
                            self.screen.blit(pts_txt, pts_txt.get_rect(center=(cx, cy)))
                    elif row_names[j]:
                        if player.board.locked[row_names[j]]:
                            pts = player.board.get_score(row_names[j])
                            pts_txt = self.font_small.render(str(pts), True, WHITE)
                            self.screen.blit(pts_txt, pts_txt.get_rect(center=(cx, cy)))
                                
                self.draw_board(
                    x + int(67 * base_scale),
                    y - int(45 * base_scale),
                    base_scale * 1.1,
                    player=player,
                    allowed=allowed
                )


            # =================================================
            # RECHTS
            # =================================================
            else:

                char_x = width - int(60 * player_scale)
                body_y = y + body_r
                head_y = y - int(15 * player_scale)

                pygame.draw.circle(self.screen, player.color, (char_x, body_y - 10), body_r)
                pygame.draw.circle(self.screen, player.color, (char_x, head_y - 10), head_r)

                is_active = (player == self.game.current_player)
                is_passive_turn = (
                    self.game.passive_phase and
                    player == self.game.passive_current_player()
                )

                if is_active:
                    name_color = (255, 215, 0)       # Gelb — würfelt gerade
                elif is_passive_turn:
                    name_color = (100, 220, 130)     # Grün — darf jetzt W+W ankreuzen
                else:
                    name_color = (220, 220, 220)     # Weiß — wartet

                self.draw_player_name(player.name, char_x, y - int(75 * player_scale), color=name_color)

                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]   # ← NEU hier definiert
                row_names    = [None, "red", "yellow", "green", "blue"]
                start_x      = x + int(-145 * player_scale)        # ← NEU wieder drin

                for j, sc in enumerate(score_colors):
                    cx = start_x + j * int(44 * player_scale)
                    cy = y - int(72 * player_scale)
                    pygame.draw.circle(self.screen, sc, (cx, cy), score_r)

                    if j == 0:
                        if player.board.penalties > 0:
                            penalty_txt = f"-{player.board.penalties * 5}"
                            pts_txt = self.font_small.render(penalty_txt, True, (120, 120, 120))
                            self.screen.blit(pts_txt, pts_txt.get_rect(center=(cx, cy)))
                    elif row_names[j]:
                        if player.board.locked[row_names[j]]:
                            pts = player.board.get_score(row_names[j])
                            pts_txt = self.font_small.render(str(pts), True, WHITE)
                            self.screen.blit(pts_txt, pts_txt.get_rect(center=(cx, cy)))

                board_scale  = base_scale * 1.1
                right_margin = int(width * 0.004)
                board_width  = int(12 * (46 * board_scale + 5))
                board_x      = width - right_margin - board_width - int(80 * player_scale)
                board_y      = y - int(45 * player_scale)

                self.draw_board(board_x, board_y, board_scale, player=player, allowed=allowed)


        # =====================================================
        # BUTTONS
        # =====================================================

        self.btn_exit  = pygame.Rect(
            width - btn_size - int(width * 0.007), 
            int(height * 0.480), 
            btn_size, btn_size
        )

        self.btn_reset = pygame.Rect(
            width - btn_size - int(width * 0.007), 
            int(height * 0.445), 
            btn_size, btn_size
        )
        
        top_y = height // 2 - dice_size - 35
        bottom_y = height // 2 + 10
        dice_bottom = bottom_y + dice_size

        shift_x = int(width * 0.21)  # 10% nach rechts

        self.btn_roll = pygame.Rect(
            width // 2 - btn_roll_w // 2 + shift_x,
            dice_bottom + int(2 * scale),
            btn_roll_w,
            btn_roll_h
        )

        self.draw_icon_button(self.btn_exit, self.icon_exit, "exit")
        self.draw_icon_button(self.btn_reset, self.icon_reset, "reset")

        can_roll = (
            self.game.rolls_this_turn < 2 and
            not self.game.marked_this_turn
        )

        if not can_roll and not (self.game.marked_this_turn or self.game.rolls_this_turn >= 2):
            # sollte nicht vorkommen
            btn_label = "WÜRFELN"
        elif self.game.rolls_this_turn == 0:
            # noch gar nicht gewürfelt
            btn_label = "WÜRFELN"
            self.confirm_reroll = False
            self.colors["roll"] = (85, 95, 90)
        elif self.game.marked_this_turn or self.game.rolls_this_turn >= 2:
            # Zug vorbei
            btn_label = "WEITER ->"
            self.confirm_reroll = False
            self.colors["roll"] = (50, 50, 50)
        elif self.confirm_reroll:
            # Bestätigung abwarten
            btn_label = "SICHER?"
            self.colors["roll"] = (180, 130, 30)   # goldgelb
        else:
            # 1x gewürfelt, noch kein Kreuz → 2. Wurf anbieten
            btn_label = "NOCHMAL?"
            self.colors["roll"] = (70, 120, 160)   # blau

        self.draw_button(self.btn_roll, btn_label, "roll", font=self.font_wuerfel_button)

        # =====================================================
        # WÜRFEL (FIXED SHIFT WIRKLICH BENUTZT)
        # =====================================================
        if not self.game.popup.active:
            roll = self.game.roll
            values = roll["values"] if roll else None

            if values:
                values = list(values.values())

            colors = [WHITE, WHITE, RED, YELLOW, GREEN, BLUE]

            # =========================
            # DICE LAYOUT (IMMER!)
            # =========================

            gap = max(15, dice_size // 6)

            bottom_total = 4 * dice_size + 3 * gap
            top_total = 2 * dice_size + gap

            shift_right = int(width * 0.21)

            bottom_start_x = ((width - bottom_total) // 2) + shift_right
            top_start_x = ((width - top_total) // 2) + shift_right

            top_y = height // 2 - dice_size - 35
            bottom_y = height // 2 - 5
            dice_bottom = bottom_y + dice_size

            for i in range(2):
                x = top_start_x + i * (dice_size + gap)
                value = values[i] if values else None

                self.draw_dice(x, top_y, dice_size, value, colors[i])

            for i in range(4):
                x = bottom_start_x + i * (dice_size + gap)
                value = values[i + 2] if values else None

                self.draw_dice(x, bottom_y, dice_size, value, colors[i + 2])

                    # Passiver Timer-Balken
            if self.game.passive_phase or self.game.active_player_phase:
                elapsed = pygame.time.get_ticks() - self.game.passive_timer
                progress = max(0.0, 1.0 - elapsed / self.game.PASSIVE_TIMEOUT)
                bar_total = int(width * 0.3)
                bar_w = int(bar_total * progress)
                bar_x = width // 2 - bar_total // 2
                bar_y = height - int(30 * scale)
                pygame.draw.rect(self.screen, (60, 60, 60), pygame.Rect(bar_x, bar_y, bar_total, int(8 * scale)), border_radius=4)
                if self.game.passive_phase:
                    pygame.draw.rect(self.screen, (240, 235, 210), pygame.Rect(bar_x, bar_y, bar_w, int(8 * scale)), border_radius=4)

                # WEITERGEBEN Button
                pass_w = int(160 * scale)
                pass_h = int(38 * scale)
                self.btn_pass = pygame.Rect(bar_x + bar_total + 20, bar_y - 15, pass_w, pass_h)
                self.colors["pass"] = (70, 100, 140)
                self.draw_button(self.btn_pass, "WEITERGEBEN", "pass", font=self.font_wuerfel_button)
            else:
                self.btn_pass = pygame.Rect(0, 0, 0, 0)

    def handle_click(self, pos):

        if self.btn_exit.collidepoint(pos):
            self.game.popup.open("exit")
            return

        if self.btn_reset.collidepoint(pos):
            self.game.popup.open("reset")
            return
        
        if self.btn_pass.collidepoint(pos):
            if self.game.passive_phase:
                self.game.passive_next()
            elif self.game.active_player_phase:
                self.game.active_player_phase = False
                self.game.popup.hide_toast()
            return

        if self.btn_roll.collidepoint(pos):
            if self.game.popup.toast_active:
                return

            zug_vorbei = self.game.marked_this_turn or self.game.rolls_this_turn >= 2

            if zug_vorbei:
                self.confirm_reroll = False
                self.game.next_turn()
                self.active_player_phase = False

            elif self.game.rolls_this_turn == 0:
                # Erster Wurf — direkt würfeln
                self.confirm_reroll = False
                self.game.roll_dice()

            elif self.confirm_reroll:
                # Bestätigt → 2. Wurf
                self.confirm_reroll = False
                self.game.roll_dice()

            else:
                # 1x gewürfelt → erst Bestätigung zeigen
                self.confirm_reroll = True

            return

        for (player_id, row_color, num), rect in self.cell_rects.items():
            if rect.collidepoint(pos):
                for player in self.game.players:
                    if id(player) == player_id:

                        if self.game.rolls_this_turn == 0:
                            break
                        if self.game.popup.toast_active and not (self.game.passive_phase or self.game.active_player_phase):
                            break

                        if player == self.game.current_player:
                            # Aktiver Spieler: erst nach passiver Phase
                            if self.game.passive_phase:
                                break
                            if not self.game.active_player_phase:
                                break
                            if self.game.marked_this_turn:
                                break
                            allowed = self.game.get_allowed_marks()
                            if num != "lock" and (row_color, num) not in allowed:
                                break
                        else:
                            # Passiver Spieler: nur wenn er gerade dran ist
                            if not self.game.passive_phase:
                                break
                            if player != self.game.passive_current_player():
                                break
                            if getattr(player, 'marked_this_round', False):
                                break
                            passive_allowed = self.game.get_allowed_marks_passive()
                            if num == "lock" or (row_color, num) not in passive_allowed:
                                break

                        if num == "lock":
                            if len(player.board.marked[row_color]) >= 5 and not player.board.locked[row_color]:
                                player.board.lock_row(row_color)
                        else:
                            if not player.board.locked[row_color]:
                                if player.board.mark(row_color, num):
                                    self.game.on_mark(player=player)
                                    player.marked_this_round = True
                                    self.confirm_reroll = False
                                    # Passiver geht automatisch weiter
                                    if player != self.game.current_player:
                                        self.game.passive_next()
                                    last_field = {"red": 12, "yellow": 12, "green": 2, "blue": 2}
                                    if num == last_field[row_color]:
                                        player.board.lock_row(row_color)
                return