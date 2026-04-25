import os
import pygame
from config import *

class Renderer:

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font_small = pygame.font.SysFont("arial", 17, bold=True)
        self.font_logo = pygame.font.SysFont("arial", 24, bold=True)

        # buttons
        self.btn_exit = pygame.Rect(0, 0, 0, 0)
        self.btn_full = pygame.Rect(0, 0, 0, 0)
        self.btn_reset = pygame.Rect(0, 0, 0, 0)
        self.btn_roll = pygame.Rect(0, 0, 0, 0)

        # icons
        self.icon_exit = pygame.image.load("assets/exit_button.png").convert_alpha()
        self.icon_full = pygame.image.load("assets/fullscreen_button.png").convert_alpha()
        self.icon_reset = pygame.image.load("assets/reset_button.png").convert_alpha()

        self.colors = {
        "exit": (180, 70, 70),        # 🔴 weiches dunkleres Rot (wie roter Würfel)
        "fullscreen": (80, 110, 190), # 🔵 dunkleres Blau (wie blauer Würfel)
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
    def draw_button(self, rect, text, key):

        color = self.colors.get(key, (100, 100, 100))

        # shadow
        shadow = rect.move(2, 2)
        pygame.draw.rect(self.screen, (0, 0, 0, 80), shadow, border_radius=12)

        # main
        pygame.draw.rect(self.screen, color, rect, border_radius=12)

        # border
        pygame.draw.rect(self.screen, (255, 255, 255, 35), rect, 1, border_radius=12)

        txt = self.font_small.render(text, True, (255, 255, 255))
        txt_shadow = self.font_small.render(text, True, (0, 0, 0))

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
            txt = self.font_big.render(
                str(value),
                True,
                (20, 20, 20) if color == WHITE else (255, 255, 255)
            )
            txt_rect = txt.get_rect(center=(x + size//2, y + size//2))
            self.screen.blit(txt, txt_rect)

        # ----------------------------
    def draw(self):

        width, height = self.screen.get_size()

        scale = width / 1400
        scale = max(0.75, min(scale, 1.2))

        btn_size = int(36 * scale)
        btn_roll_w = int(180 * scale)
        btn_roll_h = int(45 * scale)

        self.draw_text("QWIXX", width // 2, height - 30, center=True)

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
                (left_x, mid),
                (right_x, mid)
            ]

        elif count == 3:
            positions = [
                (left_x, bottom),
                (int(w * 0.45), top),
                (right_x, bottom)
            ]

        elif count == 4:
            positions = [
                (left_x, top),
                (left_x, bottom),
                (right_x, top),
                (right_x, bottom)
            ]

        elif count == 5:
            positions = [
                (left_x, top),
                (left_x, bottom),
                (int(w * 0.45), top),
                (right_x, top),
                (right_x, bottom)
            ]

        # =====================================================
        # SPIELER ZEICHNEN
        # =====================================================

        for i, player in enumerate(self.game.players):

            if i >= len(positions):
                continue

            x, y = positions[i]

            # rechte Seite?
            right_side = x > width / 2

            # -------------------------------------------------
            # LINKE SEITE NORMAL
            # -------------------------------------------------
            if not right_side:

                # BODY
                pygame.draw.circle(
                    self.screen,
                    player.color,
                    (x + 20, y + 30),
                    40
                )

                # HEAD
                pygame.draw.circle(
                    self.screen,
                    player.color,
                    (x + 20, y - 20),
                    30
                )

                # NAME
                name_text = self.font_small.render(player.name, True, WHITE)
                name_rect = name_text.get_rect(center=(x + 25, y - 70))
                self.screen.blit(name_text, name_rect)

                # SCORE LINKS -> RECHTS
                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]

                for j, color in enumerate(score_colors):

                    pygame.draw.circle(
                        self.screen,
                        color,
                        (x + 95 + j * 50, y - 70),
                        25
                    )

            # -------------------------------------------------
            # RECHTE SEITE GESPIEGELT
            # -------------------------------------------------
            else:

                # BODY
                pygame.draw.circle(
                    self.screen,
                    player.color,
                    (x + 300, y + 30),
                    40
                )

                # HEAD
                pygame.draw.circle(
                    self.screen,
                    player.color,
                    (x + 300, y - 20),
                    30
                )

                # NAME LINKS VOM KOPF
                name_text = self.font_small.render(player.name, True, WHITE)
                name_rect = name_text.get_rect(midright=(x + 330, y - 70))
                self.screen.blit(name_text, name_rect)

                # SCORE GANZ LINKS DAVON
                score_colors = [GRAY2, RED, YELLOW, GREEN, BLUE]

                for j, color in enumerate(score_colors):

                    pygame.draw.circle(
                        self.screen,
                        color,
                        (x + 29 + j * 50, y - 70),
                        25
                    )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.btn_exit = pygame.Rect(
            width - btn_size - 10,
            height - btn_size - 10,
            btn_size,
            btn_size
        )

        self.btn_full = pygame.Rect(
            width - 2 * (btn_size + 10),
            height - btn_size - 10,
            btn_size,
            btn_size
        )

        self.btn_reset = pygame.Rect(
            width - 3 * (btn_size + 10),
            height - btn_size - 10,
            btn_size,
            btn_size
        )

        self.btn_roll = pygame.Rect(
            width // 2 - btn_roll_w // 2,
            height - int(120 * scale),
            btn_roll_w,
            btn_roll_h
        )

        self.draw_icon_button(self.btn_exit, self.icon_exit, "exit")
        self.draw_icon_button(self.btn_full, self.icon_full, "fullscreen")
        self.draw_icon_button(self.btn_reset, self.icon_reset, "reset")

        self.draw_button(self.btn_roll, "WÜRFELN", "roll")

        # =====================================================
        # WÜRFEL
        # =====================================================

        roll = self.game.roll
        values = roll["values"] if roll else None

        if values:
            values = list(values.values())

        colors = [WHITE, WHITE, RED, YELLOW, GREEN, BLUE]

        base_size = 65
        dice_size = int(base_size * scale * 0.9)
        gap = max(4, dice_size // 6)

        bottom_total = 4 * dice_size + 3 * gap
        bottom_start_x = (width - bottom_total) // 2

        top_total = 2 * dice_size + gap
        top_start_x = (width - top_total) // 2

        top_y = height // 2 - dice_size - 35
        bottom_y = height // 2 + 10

        # weiße Würfel
        for i in range(2):

            x = top_start_x + i * (dice_size + gap)
            value = values[i] if values else None

            self.draw_dice(
                x,
                top_y,
                dice_size,
                value,
                colors[i]
            )

        # farbige Würfel
        for i in range(4):

            x = bottom_start_x + i * (dice_size + gap)
            value = values[i + 2] if values else None

            self.draw_dice(
                x,
                bottom_y,
                dice_size,
                value,
                colors[i + 2]
            )
    def handle_click(self, pos):

        if self.btn_exit.collidepoint(pos):
            self.game.popup.open("exit")
            return

        if self.btn_full.collidepoint(pos):
            self.screen = self.game.toggle_fullscreen()
            return

        if self.btn_reset.collidepoint(pos):
            print("🔄 RESET CLICKED")
            self.game.popup.open("reset")   # NUR POPUP ÖFFNEN
            return

        if self.btn_roll.collidepoint(pos):
            self.game.roll_dice()
            return