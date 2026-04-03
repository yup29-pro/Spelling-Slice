# menu.py — Stitch-inspired Cyberpunk Menu

import pygame
import math
from settings import *


def draw_menu(screen, font_big, font_med, font_sm, tick):
    screen.fill((10, 12, 30))

    # ── Animated scanline background ─────────────────
    for y in range(0, HEIGHT, 6):
        alpha = 18
        s = pygame.Surface((WIDTH, 1))
        s.set_alpha(alpha)
        s.fill((0, 200, 255))
        screen.blit(s, (0, y))

    # ── Big stacked title ─────────────────────────────
    t1 = font_big.render("SPELLING", True, (200, 220, 255))
    t2 = font_big.render("SLICE", True, (0, 255, 220))
    t1_x = WIDTH // 2 - t1.get_width() // 2
    t2_x = WIDTH // 2 - t2.get_width() // 2
    screen.blit(t1, (t1_x, 40))
    screen.blit(t2, (t2_x, 100))

    # ── Subtitle ──────────────────────────────────────
    sub = font_sm.render("CUT THROUGH THE LETTERS", True, (0, 220, 255))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 168))

    # ── Divider line ──────────────────────────────────
    pygame.draw.line(screen, (0, 180, 255), (60, 200), (WIDTH - 60, 200), 1)

    # ── Level cards ───────────────────────────────────
    levels = [
        {
            "key":   "beginner",
            "icon":  ":)",
            "title": "BEGINNER",
            "desc":  "Safe words, easy cuts.",
            "color": (180, 255, 100),
            "y":     220,
        },
        {
            "key":   "intermediate",
            "icon":  ":/",
            "title": "INTERMEDIATE",
            "desc":  "Faster words, trickier spellings.",
            "color": (0, 220, 255),
            "y":     360,
        },
        {
            "key":   "advanced",
            "icon":  ">:(",
            "title": "ADVANCED",
            "desc":  "Long words, high speed!",
            "color": (255, 80, 180),
            "y":     500,
        },
    ]

    rects = {}
    mouse = pygame.mouse.get_pos()

    for lvl in levels:
        card_rect = pygame.Rect(60, lvl["y"], WIDTH - 120, 120)
        hovered   = card_rect.collidepoint(mouse)

        # Card background
        bg_color = (20, 25, 55) if not hovered else (25, 35, 75)
        pygame.draw.rect(screen, bg_color, card_rect, border_radius=16)

        # Glowing border
        border_color = lvl["color"] if hovered else (40, 50, 100)
        pygame.draw.rect(screen, border_color, card_rect, 2, border_radius=16)

        # Icon circle
        icon_cx = card_rect.x + 55
        icon_cy = card_rect.centery
        pygame.draw.circle(screen, (20, 30, 60), (icon_cx, icon_cy), 32)
        pygame.draw.circle(screen, lvl["color"], (icon_cx, icon_cy), 32, 2)
        icon_surf = font_sm.render(lvl["icon"], True, lvl["color"])
        screen.blit(icon_surf, (icon_cx - icon_surf.get_width() // 2,
                                icon_cy - icon_surf.get_height() // 2))

        # Title
        title_surf = font_med.render(lvl["title"], True, (255, 255, 255))
        screen.blit(title_surf, (card_rect.x + 105, card_rect.y + 18))

        # Description
        desc_surf = font_sm.render(lvl["desc"], True, (140, 160, 200))
        screen.blit(desc_surf, (card_rect.x + 105, card_rect.y + 58))

        # START button
        btn_rect = pygame.Rect(card_rect.x + 105, card_rect.y + 82, 120, 28)
        pygame.draw.rect(screen, lvl["color"], btn_rect, border_radius=20)
        btn_txt = font_sm.render("START", True, (10, 12, 30))
        screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                              btn_rect.centery - btn_txt.get_height() // 2))

        rects[lvl["key"]] = card_rect

    return rects


def run_menu(screen, font_big, font_med, font_sm=None):
    clock = pygame.time.Clock()
    if font_sm is None:
        font_sm = pygame.font.SysFont("Arial", 22, bold=True)
    tick = 0

    while True:
        tick += 1
        rects = draw_menu(screen, font_big, font_med, font_sm, tick)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level, rect in rects.items():
                    if rect.collidepoint(event.pos):
                        return level

        clock.tick(FPS)