from dice import Dice
from moves import get_moves
from board import Board

dice = Dice()
board = Board()

reroll_used = False

while True:
    print("\n🎲 Würfeln...")
    roll = dice.roll()
    print("Wurf:", roll)

    options = get_moves(roll)
    print("\nOptionen:", options)

    board.display()

    print("\n👉 Was willst du tun?")
    
    if not reroll_used:
        action = input("mark / reroll / quit: ")
    else:
        action = input("mark / quit (kein reroll mehr erlaubt): ")

    # ❌ Spiel beenden
    if action == "quit":
        break

    # 🔁 nochmal würfeln (nur 1x erlaubt)
    if action == "reroll" and not reroll_used:
        reroll_used = True
        continue

    # 🚨 nach reroll MUSS markiert werden
    if action == "reroll" and reroll_used:
        print("❌ Kein erneutes Würfeln erlaubt!")
        continue

    #markieren
    if action == "mark":

        color = input("Farbe: ").strip().lower()
        value = int(input("Zahl: ").strip())

    if color not in ["red", "yellow", "green", "blue"]:
        print("❌ ungültige Farbe")
        continue

    if value not in options[color]:
        print("❌ nicht erlaubt (nicht in Options)")
        continue

    success = board.mark(color, value)

    if success:
        print(f"✅ {color.upper()} {value} erfolgreich markiert!")
        reroll_used = False
    else:
        print("❌ nicht erlaubt (Regel verletzt oder schon markiert)")