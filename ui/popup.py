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
        self.mode = "start"

        self.btn_yes = pygame.Rect(0, 0, 0, 0)
        self.btn_no = pygame.Rect(0, 0, 0, 0)
        self.slider_rect = pygame.Rect(0, 0, 0, 0)
        self.slider_knob = pygame.Rect(0, 0, 0, 0)

        self.player_count = 2
        self.dragging_slider = False
        self.name_inputs = []
        self.active_input = 0
        self.input_rects = []

        self.toast_active = False
        self.toast_timer = 0
        self.toast_text = ""
        self.toast_color = (220, 220, 220)
        self.toast_subtext = ""
        self.toast_subtext2 = ""

    # ---------------- OPEN ----------------
    def open(self, mode="reset"):
        self.mode = mode

        if mode == "turn_notify":
            self.active = False
            # ── NUR Spielername, kein Würfel-Text ──
            self.toast_text     = f"{self.game.current_player.name} ist dran!"
            self.toast_subtext  = "Würfeln um zu starten"   # ← kein W+W, kein Farbe-Text
            self.toast_subtext2 = ""
            self.toast_color    = self.game.current_player.color
            self.toast_timer    = pygame.time.get_ticks()
            self.toast_active   = True
            return

        self.active = True
        if mode == "names":
            self.name_inputs = [""] * self.player_count
            self.active_input = 0

    def close(self):
        self.active = False

    # ---------------- CLICK ----------------
    def handle_click(self, pos):
        if not self.active:
            return False

        # TURN NOTIFY — Klick schließt es und geht weiter
        if self.mode == "turn_notify":
            self.close()
            return False   # False = Renderer darf den Klick auch verarbeiten

        # SLIDER / START
        if self.mode == "start":
            if self.slider_rect.collidepoint(pos):
                self.dragging_slider = True
                self._update_slider(pos)
                return True
            if self.btn_yes.collidepoint(pos):
                self.open("names")
                return True
            return False

        # NAMEN
        if self.mode == "names":
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(pos):
                    self.active_input = i
                    return True
            if self.btn_yes.collidepoint(pos):
                while len(self.name_inputs) < self.player_count:
                    self.name_inputs.append(f"Player {len(self.name_inputs)+1}")
                self._start_game()
                self.close()
                return True
            return False

        # RESET
        if self.mode == "reset":
            if self.btn_yes.collidepoint(pos):
                self.game.reset_game()
                self.open("start")
                return True
            elif self.btn_no.collidepoint(pos):
                self.close()
                return True

        # EXIT
        elif self.mode == "exit":
            if self.btn_yes.collidepoint(pos):
                pygame.quit()
                raise SystemExit
            elif self.btn_no.collidepoint(pos):
                self.close()
                return True

        return False

    def handle_release(self):
        self.dragging_slider = False

    def handle_motion(self, pos):
        if not self.active:
            return
        if self.mode == "start" and self.dragging_slider:
            self._update_slider(pos)

    def handle_keydown(self, event):
        if not self.active or self.mode != "names":
            return

        while len(self.name_inputs) < self.player_count:
            self.name_inputs.append("")

        i = self.active_input

        if event.key == pygame.K_BACKSPACE:
            self.name_inputs[i] = self.name_inputs[i][:-1]
        elif event.key in (pygame.K_TAB, pygame.K_RETURN):
            self.active_input = (self.active_input + 1) % self.player_count
        elif event.unicode and len(self.name_inputs[i]) < 14:
            self.name_inputs[i] += event.unicode

    # ---------------- START GAME ----------------
    def _start_game(self):
        self.game.players.clear()

        for i in range(self.player_count):
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            name = self.name_inputs[i].strip() if i < len(self.name_inputs) and self.name_inputs[i].strip() else f"Player {i+1}"
            self.game.add_player(Player(name, color))

        print("🎮 Spiel gestartet mit", self.player_count, "Spielern")
        self.game.start_game()   # ← NEU: zufälligen Startspieler wählen + Popup

    # ---------------- SLIDER ----------------
    def _update_slider(self, pos):
        x1 = self.slider_rect.x
        x2 = self.slider_rect.right
        t = (pos[0] - x1) / (x2 - x1)
        t = max(0, min(1, t))
        stops = [2, 3, 4, 5]
        index = round(t * (len(stops) - 1))
        self.player_count = stops[max(0, min(len(stops)-1, index))]

    def update_buttons(self, width, height):
        if self.mode == "names":
            input_area_h = self.player_count * 46
            popup_h = 80 + input_area_h + 80
        else:
            popup_h = 360

        px = width // 2 - 250
        py = height // 2 - popup_h // 2
        self.btn_yes = pygame.Rect(px + 90, py + 220, 120, 50)
        self.btn_no = pygame.Rect(px + 290, py + 220, 120, 50)

    def show_roll_toast(self, white_sum):
        self.toast_text     = f"{self.game.current_player.name} ist dran!"
        self.toast_subtext  = ""   # ← wichtig!
        self.toast_subtext2 = ""   # ← wichtig!
        self.toast_color    = (240, 235, 210)
        self.toast_timer    = pygame.time.get_ticks()
        self.toast_active   = True

    def show_passive_toast(self, player_name, white_sum):
        self.toast_text    = f"{player_name}:"
        self.toast_subtext = f"Weiße Summe ({white_sum}) ankreuzen?"
        self.toast_subtext2 = ""   # ← wichtig!
        self.toast_color   = (100, 220, 130)
        self.toast_timer   = pygame.time.get_ticks()
        self.toast_active  = True

    def show_wuerfler_toast(self, player_name):
        self.toast_text = f"Der Würfler ({player_name}) ist dran!"
        self.toast_color = (255, 215, 0)   # Gelb
        self.toast_timer = pygame.time.get_ticks()
        self.toast_active = True

    def hide_toast(self):
        self.toast_active = False
        self.toast_text = ""

    def show_active_toast(self, player_name, white_sum):
        self.toast_text  = f"{player_name}: Jetzt du! W+W={white_sum} oder Farbe wählen"
        self.toast_color = (255, 215, 0)
        self.toast_timer = pygame.time.get_ticks()
        self.toast_active = True

    def show_active_color_only_toast(self, player_name, white_sum):
        self.toast_text     = f"{player_name}: Farbe wählen!"
        self.toast_subtext  = f"W+W={white_sum} oder Weiß+Farbe"
        self.toast_subtext2 = ""
        self.toast_color    = (255, 160, 50)   # Orange = kein NOCHMAL mehr
        self.toast_timer    = pygame.time.get_ticks()
        self.toast_active   = True

    # ---------------- DRAW ----------------
    def draw(self):
        w, h = self.screen.get_size()

                # ---- TOAST ZUERST — immer, auch wenn kein Popup aktiv ----
        if self.toast_active:
            now = pygame.time.get_ticks()
            elapsed = now - self.toast_timer

            is_permanent = self.game.passive_phase
            duration = 99999999 if is_permanent else 3000

            if elapsed > duration:
                self.toast_active = False
            else:
                alpha = int((elapsed / 300) * 220) if elapsed < 300 else 220

                font      = pygame.font.Font("assets/caveat-bold.ttf", max(24, int(42 * min(w/1920, h/1080))))
                font_sub  = pygame.font.Font("assets/caveat-bold.ttf", max(20, int(36 * min(w/1920, h/1080))))
                font_sub2 = pygame.font.Font("assets/caveat-bold.ttf", max(18, int(30 * min(w/1920, h/1080))))

                line1 = font.render(self.toast_text, True, self.toast_color)
                sub1  = getattr(self, "toast_subtext",  "")
                sub2  = getattr(self, "toast_subtext2", "")
                line2 = font_sub.render(sub1,  True, self.toast_color) if sub1 else None
                line3 = font_sub2.render(sub2, True, self.toast_color) if sub2 else None

                all_lines = [l for l in [line1, line2, line3] if l]
                total_w = max(l.get_width() for l in all_lines)
                total_h = sum(l.get_height() for l in all_lines) + (len(all_lines) - 1) * 4

                pad_x, pad_y = 30, 12
                bg = pygame.Surface((total_w + pad_x*2, total_h + pad_y*2), pygame.SRCALPHA)
                bg.fill((20, 20, 25, int(alpha * 0.8)))
                pygame.draw.rect(bg, (*self.toast_color, int(alpha * 0.6)), bg.get_rect(), 2, border_radius=12)

                bx = w//2 - bg.get_width()//2
                by = int(h * 0.07)
                self.screen.blit(bg, (bx, by))

                y_cursor = by + pad_y
                for line in all_lines:
                    line.set_alpha(alpha)
                    self.screen.blit(line, line.get_rect(centerx=w//2, top=y_cursor))
                    y_cursor += line.get_height() + 4
                    
        # ---- AB HIER nur wenn Popup aktiv ----
        if not self.active:
            return

        self.update_buttons(w, h)
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        # ... rest bleibt gleich

        if self.mode == "names":
            input_area_h = self.player_count * 46  # Höhe aller Eingabefelder
            popup_h = 80 + input_area_h + 80       # Titel + Felder + Button-Abstand
        else:
            popup_h = 360                          # Standard für start/reset/exit

        box = pygame.Rect(w//2 - 250, h//2 - popup_h//2, 500, popup_h)

        pygame.draw.rect(self.screen, (35, 35, 40), box, border_radius=16)
        pygame.draw.rect(self.screen, (255, 255, 255), box, 2, border_radius=16)

        # ---- START ----
        if self.mode == "start":
            title = self.font_title.render("Spieler auswählen", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(w//2, box.y + 50)))

            txt = self.font_small.render(f"{self.player_count} Spieler", True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=(w//2, box.y + 120)))

            self.slider_rect = pygame.Rect(box.x + 80, box.y + 160, 340, 8)
            pygame.draw.rect(self.screen, (80, 80, 80), self.slider_rect, border_radius=4)

            stops = [2, 3, 4, 5]
            index = stops.index(self.player_count)
            t = index / (len(stops) - 1)
            knob_x = self.slider_rect.x + t * self.slider_rect.width
            self.slider_knob = pygame.Rect(knob_x - 10, self.slider_rect.y - 6, 20, 20)
            pygame.draw.rect(self.screen, (255, 255, 255), self.slider_knob, border_radius=10)

            self.btn_yes = pygame.Rect(w//2 - 70, box.y + 240, 140, 50)
            pygame.draw.rect(self.screen, (70, 180, 90), self.btn_yes, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), self.btn_yes, 2, border_radius=12)
            txt = self.font_small.render("WEITER", True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=self.btn_yes.center))
            return

        # ---- NAMEN ----
        if self.mode == "names":
            title = self.font_title.render("Namen eingeben", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(w//2, box.y + 45)))

            self.input_rects = []

            while len(self.name_inputs) < self.player_count:
                self.name_inputs.append("")

            for i in range(self.player_count):
                rect = pygame.Rect(box.x + 80, box.y + 80 + i * 46, 340, 36)
                self.input_rects.append(rect)

                color = (80, 85, 90) if i == self.active_input else (55, 60, 65)
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=8)

                display = self.name_inputs[i] if self.name_inputs[i] else f"Player {i+1}"
                txt_color = WHITE if self.name_inputs[i] else (130, 130, 130)
                txt = self.font_small.render(display, True, txt_color)
                self.screen.blit(txt, txt.get_rect(midleft=(rect.x + 10, rect.centery)))

                if i == self.active_input and pygame.time.get_ticks() % 1000 < 500:
                    cursor_x = rect.x + 10 + txt.get_width() + 2
                    pygame.draw.line(self.screen, WHITE,
                                     (cursor_x, rect.y + 6),
                                     (cursor_x, rect.bottom - 6), 2)

            self.btn_yes = pygame.Rect(w//2 - 70, box.bottom - 65, 140, 45)
            pygame.draw.rect(self.screen, (70, 180, 90), self.btn_yes, border_radius=12)
            pygame.draw.rect(self.screen, WHITE, self.btn_yes, 2, border_radius=12)
            txt = self.font_small.render("START", True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=self.btn_yes.center))
            return

        # ---- RESET / EXIT ----
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