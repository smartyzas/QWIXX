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

    def draw_board(self, x, y, scale=1.0):

            row_h = int(38 * scale)
            cell_w = int(46 * scale)
            gap = 5

            colors = [
                (200, 70, 70),     # rot
                (230, 210, 60),    # gelb
                (70, 170, 70),     # grün
                (70, 110, 220)     # blau
            ]

            rows = [
                list(range(2, 13)),
                list(range(2, 13)),
                list(range(12, 1, -1)),
                list(range(12, 1, -1))
            ]

            for r in range(4):

                row_y = y + r * (row_h + gap)

                for i, num in enumerate(rows[r]):

                    rect = pygame.Rect(
                        x + i * (cell_w + gap),
                        row_y,
                        cell_w,
                        row_h
                    )

                    pygame.draw.rect(self.screen, colors[r], rect, border_radius=5)
                    pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=5)

                    txt = self.font_small.render(str(num), True, BLACK)
                    txt_rect = txt.get_rect(center=rect.center)
                    self.screen.blit(txt, txt_rect)

                # Schloss Feld rechts
                lock_rect = pygame.Rect(
                    x + 11 * (cell_w + gap) + 8,
                    row_y,
                    row_h,
                    row_h
                )

                pygame.draw.rect(self.screen, (128, 110, 108), lock_rect, border_radius=5)
                pygame.draw.rect(self.screen, WHITE, lock_rect, 1, border_radius=5)

                # NEU (richtig):
                padding = 4
                icon_size = lock_rect.width - padding * 2
                lock_img = pygame.transform.smoothscale(self.icon_lock_field, (icon_size, icon_size))
                lock_img_rect = lock_img.get_rect(center=lock_rect.center)
                self.screen.blit(lock_img, lock_img_rect)


    def draw_player_name(self, name, char_x, base_y):
        if len(name) <= 9:
            txt = self.font_small.render(name, True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=(char_x, base_y)))
            return txt.get_rect(center=(char_x, base_y))
        else:
            line1 = name[:9] + "-"
            line2 = name[9:]
            line_h = self.font_small.size("A")[1]
            gap = 3  # ← kleiner Puffer zwischen den Zeilen

            txt1 = self.font_small.render(line1, True, WHITE)
            txt2 = self.font_small.render(line2, True, WHITE)

            # Gesamthöhe = 2 Zeilen + gap, dann mittig auf base_y zentrieren
            total_h = line_h * 2 + gap
            y1 = base_y - total_h // 2 + line_h // 2
            y2 = y1 + line_h + gap

            self.screen.blit(txt1, txt1.get_rect(center=(char_x, y1)))
            self.screen.blit(txt2, txt2.get_rect(center=(char_x, y2)))

            return txt1.get_rect(center=(char_x, y1))
        
 #-----------------------------------------
    def draw(self):

        if self.game.popup.active:
            return
        width, height = self.screen.get_size()

        scale = width / 1400
        scale = max(0.75, min(scale, 1.2))

        base_scale = min(width / 1400, height / 900)
        base_scale = max(0.7, min(base_scale, 1.4))

        btn_size = int(36 * scale)
        btn_roll_w = int(180 * scale)
        btn_roll_h = int(45 * scale)

        # QWIXX Titel (wie gehabt)
        
        txt_qwixx = self.font_logo.render("QWIXX", True, (220, 220, 220))
        rect_qwixx = txt_qwixx.get_rect(center=(width - btn_size // 2 - 215, height - btn_size - 545))
        self.screen.blit(txt_qwixx, rect_qwixx)

        # ← NEU: "für Leni" darunter, kleinere Font
        txt = self.font_logo_small.render("Leni Edition", True, (220, 220, 220))
        rect = txt.get_rect(center=(
            width - btn_size // 2 - 215,   # gleiche X-Position wie QWIXX
            height - btn_size - 495        # etwas tiefer (z.B. +45px)
        ))
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

        top = int(h * 0.15)
        bottom = int(h * 0.60)
        mid = int(h * 0.35)

        positions = []

        if count == 2:
            positions = [
                (left_x, mid - 100),
                (left_x, mid + 300)
            ]

        elif count == 3:
            positions = [
                (left_x, top + 10),    #1
                (left_x, top + 360),   #2
                (left_x, top + 700),   #3
            ]

        elif count == 4:
            positions = [
                (left_x, top + 10),    #1
                (left_x, top + 360),   #2
                (left_x, top + 700),   #3
                (right_x, top + 10),   #4
            ]

        elif count == 5:
            positions = [
                (left_x, top + 10),    #1
                (left_x, top + 360),   #2
                (left_x, top + 700),   #3
                (right_x, top + 10),   #4
                (right_x, top + 700),  #5
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

            # =================================================
            # LINKS
            # =================================================
            if not right_side:

                char_x = x + body_r - 10
                body_y = y + body_r
                head_y = y - int(15 * player_scale)

                pygame.draw.circle(self.screen, player.color,
                                (char_x, body_y - 10), body_r)

                pygame.draw.circle(self.screen, player.color,
                                (char_x, head_y - 10), head_r)

                name_rect = self.draw_player_name(
                    player.name,
                    char_x,
                    y - int(58 * player_scale) - 15
                )

                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]

                start_x = x + int(300 * player_scale)

                for j, color in enumerate(score_colors):
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (
                            start_x + j * int(44 * player_scale) - 10,
                            y - int(72 * player_scale)
                        ),
                        score_r
                    )

                board_scale = base_scale * 1.1

                self.draw_board(
                    x + int(60 * base_scale),
                    y - int(45 * base_scale),
                    board_scale
                )

            # =================================================
            # RECHTS
            # =================================================
            else:

                char_x = width - int(60 * player_scale)
                body_y = y + body_r
                head_y = y - int(15 * player_scale)

                pygame.draw.circle(self.screen, player.color,
                                (char_x, body_y - 10), body_r)

                pygame.draw.circle(self.screen, player.color,
                                (char_x, head_y - 10), head_r)

                name_rect = self.draw_player_name(
                    player.name,
                    char_x,
                    y - int(58 * player_scale) - 15
                )

                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]

                start_x = width - int(510 * player_scale)

                for j, color in enumerate(score_colors):
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (
                            start_x + j * int(44 * player_scale) - 1,
                            y - int(72 * player_scale)
                        ),
                        score_r
                    )

                # ✅ FIX: stabiles Board rechts
                board_scale = base_scale * 1.1

                right_margin = int(width * 0.004)
                board_width = int(12 * (46 * board_scale + 5))

                board_x = width - right_margin - board_width - int(80 * player_scale)
                board_y = y - int(45 * player_scale)

                self.draw_board(board_x, board_y, board_scale)

        # =====================================================
        # BUTTONS
        # =====================================================

        self.btn_exit = pygame.Rect(
            width - btn_size - 10,
            height - btn_size - 525,
            btn_size,
            btn_size
        )

        self.btn_reset = pygame.Rect(
            width - btn_size - 10,
            height - btn_size - 570,
            btn_size,
            btn_size
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

        self.draw_button(self.btn_roll, "WÜRFELN", "roll", font=self.font_wuerfel_button)

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

    def handle_click(self, pos):

        if self.btn_exit.collidepoint(pos):
            self.game.popup.open("exit")
            return

        if self.btn_reset.collidepoint(pos):
            print("🔄 RESET CLICKED")
            self.game.popup.open("reset")   # NUR POPUP ÖFFNEN
            return

        if self.btn_roll.collidepoint(pos):
            self.game.roll_dice()
            return