import pygame
import sys
from ui.popup import Popup

print("🚀 START main.py wird ausgeführt...")

from game.game import Game
from game.player import Player
from ui.renderer import Renderer
from config import BG_COLOR

pygame.init()

print("🎮 Pygame initialisiert")

screen = pygame.display.set_mode((1400, 900), pygame.RESIZABLE)
pygame.display.set_caption("QWIXX")

print("🪟 Fenster erstellt")

clock = pygame.time.Clock()

game = Game()

popup = Popup(screen, game)
game.popup = popup   # 🔥 WICHTIG

renderer = Renderer(screen, game)

print("🧠 Game + Renderer erstellt")

# TEST PLAYERS
game.add_player(Player("Matas"))
game.add_player(Player("Leni"))

print("👥 Spieler hinzugefügt")

running = True

while running:

    screen.fill(BG_COLOR)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print("❌ Fenster geschlossen")
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.popup.handle_click(event.pos)
            renderer.handle_click(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("🎲 Würfeln via SPACE")
                game.roll_dice()

    game.update()
    renderer.draw()
    game.popup.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()