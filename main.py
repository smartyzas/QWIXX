import os
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

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

print("🪟 Fenster erstellt")

clock = pygame.time.Clock()

game = Game()

popup = Popup(screen, game)
game.popup = popup   # 🔥 WICHTIG
popup.open("start")   # 🔥 START POPUP AUTO

renderer = Renderer(screen, game)
import inspect
print(inspect.getsourcefile(renderer.handle_click))
print(inspect.getsource(renderer.handle_click)[:200])

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
            if not popup.handle_click(event.pos):
                renderer.handle_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            game.popup.handle_release()

        elif event.type == pygame.MOUSEMOTION:
            game.popup.handle_motion(event.pos)

        elif event.type == pygame.KEYDOWN:
            game.popup.handle_keydown(event)

            if event.key == pygame.K_SPACE:
                renderer.handle_click(pygame.mouse.get_pos())  # ← nur einmal

            elif event.key == pygame.K_m:
                import ctypes
                hwnd = pygame.display.get_wm_info()["window"]
                ctypes.windll.user32.ShowWindow(hwnd, 9)
                screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                renderer.screen = screen
                popup.screen = screen

            elif event.key == pygame.K_f:
                import ctypes
                hwnd = pygame.display.get_wm_info()["window"]
                ctypes.windll.user32.ShowWindow(hwnd, 9)
                pygame.display.quit()
                pygame.display.init()
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                renderer.screen = screen
                popup.screen = screen

            elif event.key == pygame.K_ESCAPE:
                game.popup.open("exit")

            elif event.key == pygame.K_r:
                game.popup.open("reset")

        elif event.type == pygame.VIDEORESIZE and not game.fullscreen:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            renderer.screen = screen
            popup.screen = screen

    # ← NUR EINMAL pro Frame, außerhalb des Event-Loops
    game.update()
    renderer.draw()
    game.popup.draw()

    pygame.display.flip()
    clock.tick(60)