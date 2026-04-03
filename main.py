# main.py — Entry point, runs the game

import pygame
from settings import *
from menu import run_menu
from game import run_game

def main():
    pygame.init()
    pygame.mixer.init()

    screen   = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    font_big = pygame.font.SysFont("Arial", 62, bold=True)
    font_med = pygame.font.SysFont("Arial", 36, bold=True)
    font_sm  = pygame.font.SysFont("Arial", 22, bold=True)

    while True:
        level = run_menu(screen, font_big, font_med, font_sm)
        score = 0

        while True:
            result, score = run_game(screen, level, score)
            if result == "menu":
                break
            elif result == "retry":
                score = 0
                continue

if __name__ == "__main__":
    main()