# game.py — Core slicing game logic

import pygame
import random
import os
import threading
import time
from gtts import gTTS
from settings import *
from words import get_word


def speak(text):
    def _speak():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            path = f"assets/sounds/temp_{int(time.time())}.mp3"
            tts = gTTS(text=text, lang='en', slow=True)
            tts.save(path)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception as e:
            print("Audio error:", e)
    threading.Thread(target=_speak, daemon=True).start()


# ── Particle System ───────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x      = float(x)
        self.y      = float(y)
        self.color  = color
        self.vx     = random.uniform(-4, 4)
        self.vy     = random.uniform(-6, -1)
        self.life   = 30
        self.radius = random.randint(3, 7)

    def update(self):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.3  # gravity
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = max(0, self.life * 8)
            pygame.draw.circle(screen, self.color,
                               (int(self.x), int(self.y)), self.radius)


# ── Letter Tile ───────────────────────────────────────────────
class LetterTile:
    def __init__(self, char, x, y, speed_x, speed_y):
        self.char        = char
        self.x           = float(x)
        self.y           = float(y)
        self.speed_x     = speed_x
        self.speed_y     = speed_y
        self.size        = TILE_SIZE
        self.alive       = True
        self.state       = "normal"
        self.flash_timer = 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def update(self):
        if self.alive:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.x <= 0 or self.x >= WIDTH - self.size:
                self.speed_x *= -1
            if self.y <= 0 or self.y >= HEIGHT - self.size:
                self.speed_y *= -1
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0 and self.state == "wrong":
                self.state = "normal"

    def draw(self, screen, font):
        if not self.alive:
            return
        if self.state == "correct":
            color = GREEN
        elif self.state == "wrong":
            color = RED
        else:
            color = YELLOW
        pygame.draw.rect(screen, color, self.get_rect(), border_radius=10)
        pygame.draw.rect(screen, WHITE, self.get_rect(), 2, border_radius=10)
        label = font.render(self.char, True, BLACK)
        screen.blit(label, (
            int(self.x) + self.size // 2 - label.get_width() // 2,
            int(self.y) + self.size // 2 - label.get_height() // 2
        ))


def line_hits_rect(p1, p2, rect):
    return bool(rect.clipline(p1, p2))


def spawn_tiles(word, speed):
    all_letters = list(word)
    distractors = random.sample(
        [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in word],
        min(6, 26 - len(set(word)))
    )
    all_letters += distractors
    random.shuffle(all_letters)
    tiles = []
    for char in all_letters:
        x  = random.randint(50, WIDTH - 100)
        y  = random.randint(50, HEIGHT - 200)
        sx = random.choice([-1, 1]) * speed
        sy = random.choice([-1, 1]) * speed
        tiles.append(LetterTile(char, x, y, sx, sy))
    return tiles


def draw_word_slots(screen, word, collected, font_med):
    total_w = len(word) * 60
    start_x = WIDTH // 2 - total_w // 2
    y = HEIGHT - 100
    for i, char in enumerate(word):
        x    = start_x + i * 60
        rect = pygame.Rect(x, y, 50, 55)
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        if i < len(collected):
            letter = font_med.render(collected[i], True, CYAN)
            screen.blit(letter, (
                x + 25 - letter.get_width() // 2,
                y + 27 - letter.get_height() // 2
            ))
        else:
            pygame.draw.line(screen, WHITE, (x + 5, y + 50), (x + 45, y + 50), 2)


def draw_hearts(screen, font, hearts):
    for i in range(4):
        color  = RED  if i < hearts else GRAY
        symbol = "♥" if i < hearts else "♡"
        heart  = font.render(symbol, True, color)
        screen.blit(heart, (WIDTH - 180 + i * 38, 50))


def draw_slice_trail(screen, trail):
    if len(trail) < 2:
        return
    for i in range(1, len(trail)):
        pygame.draw.line(screen, WHITE, trail[i-1], trail[i], 3)


def draw_timer(screen, font, time_left):
    """Draw countdown timer — turns red when low"""
    color = RED if time_left <= 10 else CYAN
    timer_surf = font.render(f"⏱ {int(time_left)}s", True, color)
    screen.blit(timer_surf, (WIDTH // 2 - timer_surf.get_width() // 2, 20))


def draw_score(screen, font, score):
    """Draw score top left"""
    score_surf = font.render(f"Score: {score}", True, NEON_YELLOW)
    screen.blit(score_surf, (20, 20))


def run_game(screen, level, total_score=0):
    clock      = pygame.time.Clock()
    font_big   = pygame.font.SysFont("Arial", 52, bold=True)
    font_med   = pygame.font.SysFont("Arial", 36, bold=True)
    font_sm    = pygame.font.SysFont("Arial", 28)
    font_heart = pygame.font.SysFont("Segoe UI Emoji", 32)

    # Timer per level
    time_limits = {
        "beginner":     45,
        "intermediate": 35,
        "advanced":     25,
    }

    word       = get_word(level)
    speed      = LEVEL_SPEED[level]
    tiles      = spawn_tiles(word, speed)
    collected  = []
    particles  = []
    trail      = []
    dragging   = False
    last_pos   = None
    won        = False
    hearts     = 4
    game_over  = False
    score      = total_score
    time_limit = time_limits[level]
    start_time = time.time()

    while True:
        screen.fill(BG_COLOR)
        elapsed   = time.time() - start_time
        if not won and not game_over:
            time_left = max(0, time_limit - elapsed)

        # ── Timeout ──────────────────────────────────────
        if time_left <= 0 and not won:
            game_over = True

        # ── Events ───────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu", score

            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                last_pos = event.pos
                trail    = [event.pos]

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                trail    = []
                last_pos = None

            if event.type == pygame.MOUSEMOTION and dragging:
                current_pos = event.pos
                trail.append(current_pos)
                if len(trail) > 20:
                    trail.pop(0)

                if last_pos and not won and not game_over:
                    for tile in tiles:
                        if tile.alive and line_hits_rect(last_pos, current_pos, tile.get_rect()):
                            needed = word[len(collected)] if len(collected) < len(word) else None
                            if tile.char == needed:
                                # ✅ Correct
                                tile.alive = False
                                tile.state = "correct"
                                collected.append(tile.char)
                                score += 10
                                # Spawn green particles
                                cx = int(tile.x) + tile.size // 2
                                cy = int(tile.y) + tile.size // 2
                                for _ in range(12):
                                    particles.append(Particle(cx, cy, GREEN))
                            else:
                                # ❌ Wrong
                                if tile.state != "wrong":
                                    tile.state       = "wrong"
                                    tile.flash_timer = 30
                                    hearts          -= 1
                                    score            = max(0, score - 5)
                                    # Spawn red particles
                                    cx = int(tile.x) + tile.size // 2
                                    cy = int(tile.y) + tile.size // 2
                                    for _ in range(10):
                                        particles.append(Particle(cx, cy, RED))
                                    if hearts <= 0:
                                        game_over = True

                last_pos = current_pos

        # ── Update ───────────────────────────────────────
        for tile in tiles:
            tile.update()

        particles = [p for p in particles if p.life > 0]
        for p in particles:
            p.update()

        # ── Draw tiles ───────────────────────────────────
        for tile in tiles:
            tile.draw(screen, font_big)

        # ── Draw particles ───────────────────────────────
        for p in particles:
            p.draw(screen)

        draw_slice_trail(screen, trail)
        draw_word_slots(screen, word, collected, font_med)
        draw_hearts(screen, font_heart, hearts)
        draw_timer(screen, font_sm, time_left)
        draw_score(screen, font_sm, score)

        # Score top left
        score_surf = font_sm.render(f"Score: {score}", True, NEON_YELLOW)
        screen.blit(score_surf, (20, 20))

        # Spell hint
        hint = font_sm.render(f"Spell:  {word}", True, WHITE)
        screen.blit(hint, (20, 55))

        # Level label
        level_txt = font_sm.render(f"Level: {level.upper()}", True, CYAN)
        screen.blit(level_txt, (20, 90))

        esc_txt = font_sm.render("ESC = Menu", True, GRAY)
        screen.blit(esc_txt, (WIDTH - 150, 85))

        # ── Win ──────────────────────────────────────────
        if collected == list(word) and not won:
            won    = True
            bonus  = max(0, int(time_left) * 2)
            score += bonus
            full_text = " ".join(list(word)) + ". " + word + ". Great job!"
            speak(full_text)

        if won:
            win_surf = font_big.render(f"  {word}!", True, GREEN)
            screen.blit(win_surf, (
                WIDTH // 2 - win_surf.get_width() // 2,
                HEIGHT // 2 - 80
            ))
            bonus_txt = font_med.render(f"Time Bonus: +{max(0, int(time_left)*2)} pts!", True, YELLOW)
            screen.blit(bonus_txt, (WIDTH // 2 - bonus_txt.get_width() // 2, HEIGHT // 2 - 20))
            msg = font_med.render("SPACE = Next word  |  ESC = Menu", True, YELLOW)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 30))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return "next", score
            if keys[pygame.K_ESCAPE]:
                return "menu", score

        # ── Game Over ────────────────────────────────────
        if game_over and not won:
            over_surf = font_big.render("GAME OVER!", True, RED)
            screen.blit(over_surf, (
                WIDTH // 2 - over_surf.get_width() // 2,
                HEIGHT // 2 - 60
            ))
            final = font_med.render(f"Final Score: {score}", True, YELLOW)
            screen.blit(final, (WIDTH // 2 - final.get_width() // 2, HEIGHT // 2))
            msg = font_med.render("SPACE = Try again  |  ESC = Menu", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return "retry", score
            if keys[pygame.K_ESCAPE]:
                return "menu", score

        pygame.display.flip()
        clock.tick(FPS)