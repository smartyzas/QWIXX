import pygame
from config import *
from game.player import Player
from config import PLAYER_COLORS



class Popup:

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.font_title = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20, bold=True)

        self.active = True
        self.mode = "start"   # 🔥 START POPUP STANDARD

        self.btn_yes = pygame.Rect(0, 0, 0, 0)
        self.btn_no = pygame.Rect(0, 0, 0, 0)
        self.slider_rect = pygame.Rect(0, 0, 0, 0)
        self.slider_knob = pygame.Rect(0, 0, 0, 0)

        self.player_count = 2  # default
        self.dragging_slider = False

    # ---------------- OPEN ----------------
    def open(self, mode="reset"):
        print("POPUP OPEN:", mode)
        self.active = True
        self.mode = mode

    def close(self):
        self.active = False

    # ---------------- CLICK ----------------
    def handle_click(self, pos):

        if not self.active:
            return False

        # ---------------- SLIDER ----------------
        if self.mode == "start":

            if self.slider_rect.collidepoint(pos):
                self.dragging_slider = True
                self._update_slider(pos)
                return True

            if self.btn_yes.collidepoint(pos):

                for i in range(self.player_count):
                    color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
                    self.game.add_player(Player(f"Player {i+1}", color))

                self._start_game()
                self.close()
                return True

            return False
        
        # ---------------- RESET / EXIT ----------------
        if self.mode == "reset":

            if self.btn_yes.collidepoint(pos):

                self.game.reset_game()

                # 👉 WICHTIG: danach START SCREEN
                self.open("start")

                return True       # sicherstellen dass Popup offen bleibt

        elif self.mode == "exit":
            pygame.quit()
            raise SystemExit

        self.close()
        return True

        
    def handle_release(self):
        self.dragging_slider = False

    def handle_motion(self, pos):

        if not self.active:
            return

        if self.mode == "start" and self.dragging_slider:
            self._update_slider(pos)

    # ---------------- START GAME ----------------
    def _start_game(self):

        self.game.players.clear()

        for i in range(self.player_count):
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            self.game.add_player(Player(f"Player {i+1}", color))

        print("🎮 Spiel gestartet mit", self.player_count, "Spielern")

    # ---------------- SLIDER ----------------
    def _update_slider(self, pos):

        x1 = self.slider_rect.x
        x2 = self.slider_rect.right

        t = (pos[0] - x1) / (x2 - x1)
        t = max(0, min(1, t))

        # 🔥 4 feste Stops: 2,3,4,5
        stops = [2, 3, 4, 5]

        index = round(t * (len(stops) - 1))
        index = max(0, min(len(stops) - 1, index))

        self.player_count = stops[index]

    def update_buttons(self, width, height):

        popup_w, popup_h = 500, 360
        px = width // 2 - popup_w // 2
        py = height // 2 - popup_h // 2

        btn_w, btn_h = 120, 50

        self.btn_yes = pygame.Rect(px + 90, py + 220, btn_w, btn_h)
        self.btn_no = pygame.Rect(px + 290, py + 220, btn_w, btn_h)

    # ---------------- DRAW ----------------
    def draw(self):

        if not self.active:
            return

        w, h = self.screen.get_size()

        self.update_buttons(w, h)  # 🔥 WICHTIG

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(w//2 - 250, h//2 - 180, 500, 360)

        pygame.draw.rect(self.screen, (35, 35, 40), box, border_radius=16)
        pygame.draw.rect(self.screen, (255, 255, 255), box, 2, border_radius=16)

        # ---------------- START MODE ----------------
        if self.mode == "start":

            title = self.font_title.render("Spieler auswählen", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(w//2, box.y + 50)))

            # TEXT
            txt = self.font_small.render(
                f"{self.player_count} Spieler",
                True,
                WHITE
            )
            self.screen.blit(txt, txt.get_rect(center=(w//2, box.y + 120)))

            # SLIDER BAR
            self.slider_rect = pygame.Rect(box.x + 80, box.y + 160, 340, 8)
            pygame.draw.rect(self.screen, (80, 80, 80), self.slider_rect, border_radius=4)

            # KNOB POSITION
            stops = [2, 3, 4, 5]

            index = stops.index(self.player_count)
            t = index / (len(stops) - 1)

            knob_x = self.slider_rect.x + t * self.slider_rect.width

            self.slider_knob = pygame.Rect(knob_x - 10, self.slider_rect.y - 6, 20, 20)

            pygame.draw.rect(self.screen, (255, 255, 255), self.slider_knob, border_radius=10)

            # START BUTTON
            self.btn_yes = pygame.Rect(w//2 - 70, box.y + 240, 140, 50)

            pygame.draw.rect(self.screen, (70, 180, 90), self.btn_yes, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), self.btn_yes, 2, border_radius=12)

            txt = self.font_small.render("START", True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=self.btn_yes.center))

            return

        # ---------------- RESET / EXIT ----------------
        if self.mode in ("reset", "exit"):

            text = "Neu starten?" if self.mode == "reset" else "Spiel verlassen?"

            title = self.font_title.render(text, True, WHITE)
            self.screen.blit(title, title.get_rect(center=(w//2, box.y + 90)))

            self.btn_yes = pygame.Rect(w//2 - 160, box.y + 200, 120, 50)
            self.btn_no = pygame.Rect(w//2 + 40, box.y + 200, 120, 50)

            pygame.draw.rect(self.screen, (70, 180, 90), self.btn_yes, border_radius=12)
            pygame.draw.rect(self.screen, (200, 70, 70), self.btn_no, border_radius=12)

            for btn, label in [(self.btn_yes, "JA"), (self.btn_no, "NEIN")]:
                pygame.draw.rect(self.screen, (255, 255, 255), btn, 2, border_radius=12)
                txt = self.font_small.render(label, True, WHITE)
                self.screen.blit(txt, txt.get_rect(center=btn.center))