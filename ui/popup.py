import pygame
from config import *

class Popup:

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.font_title = pygame.font.SysFont("arial", 26, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18, bold=True)

        self.active = False

        self.btn_yes = pygame.Rect(0, 0, 0, 0)
        self.btn_no = pygame.Rect(0, 0, 0, 0)

    # ----------------------------
    def open(self):
        self.active = True

    def close(self):
        self.active = False

    # ----------------------------
    def handle_click(self, pos):

        if not self.active:
            return

        if self.btn_yes.collidepoint(pos):
            self.game.reset_game()
            self.close()

        elif self.btn_no.collidepoint(pos):
            self.close()

    # ----------------------------
    def draw(self):

        if not self.active:
            return

        width, height = self.screen.get_size()

        # Overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Popup Box
        popup_w, popup_h = 420, 240

        px = width // 2 - popup_w // 2
        py = height // 2 - popup_h // 2

        rect = pygame.Rect(px, py, popup_w, popup_h)

        pygame.draw.rect(self.screen, (35, 45, 50), rect, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=12)

        # ---------------- TEXT (2 Zeilen)
        line1 = self.font_title.render(
            "Wollt ihr das Spiel wirklich",
            True,
            WHITE
        )

        line2 = self.font_title.render(
            "neu starten?",
            True,
            WHITE
        )

        rect1 = line1.get_rect(center=(width // 2, py + 60))
        rect2 = line2.get_rect(center=(width // 2, py + 95))

        self.screen.blit(line1, rect1)
        self.screen.blit(line2, rect2)

        # ---------------- BUTTONS
        btn_w, btn_h = 120, 45

        self.btn_yes = pygame.Rect(px + 60, py + 155, btn_w, btn_h)
        self.btn_no = pygame.Rect(px + 240, py + 155, btn_w, btn_h)

        self._draw_button(self.btn_yes, "Ja", (80, 160, 80))
        self._draw_button(self.btn_no, "Nein", (180, 80, 80))

    # ----------------------------
    def _draw_button(self, rect, text, color):

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=10)

        txt = self.font_small.render(text, True, WHITE)
        txt_rect = txt.get_rect(center=rect.center)

        self.screen.blit(txt, txt_rect)