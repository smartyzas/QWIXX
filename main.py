import pygame
import sys
from ui.popup import Popup
from config import *

print("🚀 START main.py wird ausgeführt...")

from game.game import Game
from game.player import Player
from ui.renderer import Renderer
from config import BG_COLOR
print(Renderer.__module__)
# print(ui.renderer.__file__)  # Uncomment for debugging if needed
pygame.init()

print("🎮 Pygame initialisiert")

screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
pygame.display.set_caption("QWIXX")

print("🪟 Fenster erstellt")

clock = pygame.time.Clock()

game = Game()

popup = Popup(screen, game)
game.popup = popup   # 🔥 WICHTIG
popup.open("start")   # 🔥 START POPUP AUTO

renderer = Renderer(screen, game)

print("🧠 Game + Renderer erstellt")

print("👥 Spieler hinzugefügt")

running = True

running = True

while running:

    screen.fill(BG_COLOR)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if game.popup.active:
                game.popup.handle_click(event.pos)

            else:
                renderer.handle_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            game.popup.handle_release()

        elif event.type == pygame.MOUSEMOTION:
            game.popup.handle_motion(event.pos)

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                game.roll_dice()

            elif event.key == pygame.K_ESCAPE and game.fullscreen:
                game.toggle_fullscreen()

        elif event.type == pygame.VIDEORESIZE and not game.fullscreen:

            screen = pygame.display.set_mode(
                (event.w, event.h),
                pygame.RESIZABLE
            )

            renderer.screen = screen
            popup.screen = screen

    # ---------------- DRAW ----------------
    game.update()
    renderer.draw()
    game.popup.draw()

    pygame.display.flip()
    clock.tick(60)