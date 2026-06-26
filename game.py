import pygame
import script
from maze import Maze
from player import Player
from ghost import Ghost
from settings import *

FONT_BITMAPS = {
    'A': [0b01110, 0b10001, 0b11111, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b11110, 0b10001, 0b11110],
    'C': [0b01111, 0b10000, 0b10000, 0b10000, 0b01111],
    'D': [0b11100, 0b10010, 0b10010, 0b10010, 0b11100],
    'E': [0b11111, 0b10000, 0b11110, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b11110, 0b10000, 0b10000],
    'G': [0b01111, 0b10000, 0b10111, 0b10001, 0b01111],
    'H': [0b10001, 0b10001, 0b11111, 0b10001, 0b10001],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b01110],
    'J': [0b00111, 0b00010, 0b00010, 0b10010, 0b01100],
    'K': [0b10001, 0b10010, 0b11100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10001, 0b10001],
    'N': [0b10001, 0b11001, 0b10101, 0b10011, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b11110, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b11110, 0b10010, 0b10001],
    'S': [0b01111, 0b10000, 0b01110, 0b00001, 0b11110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10101, 0b11011, 0b10001],
    'X': [0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    'Y': [0b10001, 0b01010, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
    '0': [0b01110, 0b10011, 0b10101, 0b11001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b01110],
    '2': [0b11110, 0b00001, 0b01110, 0b10000, 0b11111],
    '3': [0b11111, 0b00010, 0b01110, 0b00001, 0b11110],
    '4': [0b10001, 0b10001, 0b11111, 0b00001, 0b00001],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b11110],
    '6': [0b01111, 0b10000, 0b11110, 0b10001, 0b01110],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b00100],
    '8': [0b01110, 0b10001, 0b01110, 0b10001, 0b01110],
    '9': [0b01110, 0b10001, 0b01111, 0b00001, 0b11110],
    ' ': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    ':': [0b00000, 0b01100, 0b00000, 0b01100, 0b00000],
    '!': [0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
    '-': [0b00000, 0b00000, 0b11110, 0b00000, 0b00000],
    '/': [0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
}

def draw_pixel_text(screen, text, x, y, scale=2, color=(255, 255, 255)):
    text = str(text).upper()
    char_w = 5 * scale
    spacing = 1 * scale
    total_w = len(text) * char_w + (len(text) - 1) * spacing
    start_x = x - total_w // 2

    current_x = start_x
    for char in text:
        bitmap = FONT_BITMAPS.get(char, FONT_BITMAPS[' '])
        for r_idx, row in enumerate(bitmap):
            for c_idx in range(5):
                if (row >> (4 - c_idx)) & 1:
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            current_x + c_idx * scale,
                            y + r_idx * scale,
                            scale,
                            scale
                        )
                    )
        current_x += char_w + spacing


class Game:
    def __init__(self, sfx_manager):
        self.sfx = sfx_manager
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.game_won = False
        self.frame_count = 0
        self.maze = Maze()
        self.player = Player(9, 8)
        self.ghosts = [
            Ghost(1, 1, R, "Blinky"),
            Ghost(12, 1, PINK, "Pinky"),
            Ghost(1, 8, CYAN, "Inky"),
            Ghost(12, 8, ORANGE, "Clyde")
        ]
        self.sfx.stop_bgm()
        self.sfx.play_start()
        self.bgm_start_time = pygame.time.get_ticks() + 850
        self.bgm_started = False
        self.select_pressed_last = False
        self.select_press_count = 0

    def pellets_remaining(self):
        count = 0
        for row in self.maze.map:
            for cell in row:
                if cell in (".", "o"):
                    count += 1
        return count

    def update(self):
        self.frame_count += 1
        if not self.bgm_started and pygame.time.get_ticks() >= self.bgm_start_time:
            self.sfx.start_bgm()
            self.bgm_started = True

        select_currently_pressed = script.pressed("SELECT")
        if select_currently_pressed and not self.select_pressed_last:
            self.select_press_count += 1
            if self.select_press_count >= 3:
                self.ghosts = []
                self.sfx.play_power_eat()
                self.select_press_count = 0
        self.select_pressed_last = select_currently_pressed

        if self.game_over or self.game_won:
            if script.pressed("START"):
                self.reset_game()
            return

        self.player.input()
        self.player.update(self.maze, self.sfx)

        if self.player.state == "game_over":
            self.game_over = True
            return

        if self.pellets_remaining() == 0:
            self.game_won = True
            self.sfx.stop_bgm()
            self.sfx.play_victory()
            return

        if self.player.state in ("alive", "respawning"):
            for ghost in self.ghosts:
                ghost.update(self.maze)

            if self.player.state == "alive":
                for ghost in self.ghosts:
                    if ghost.row == self.player.row and ghost.col == self.player.col:
                        self.player.trigger_death(self.sfx)
                        break

    def draw(self, screen):
        try:
            if self.game_over:
                pygame.display.set_caption(f"Pacman - GAME OVER | SCORE: {self.player.score}")
            elif self.game_won:
                pygame.display.set_caption(f"Pacman - VICTORY WW! | SCORE: {self.player.score}")
            else:
                pygame.display.set_caption(
                    f"Pacman - SCORE: {self.player.score} | LIVES: {self.player.lives}")
        except Exception:
            pass

        def safe_render(text, size, color):
            try:
                font = pygame.font.Font(None, size)
                return font.render(text, True, color)
            except Exception:
                return None

        if self.game_over:
            screen.fill((0, 0, 0))
            text_go = safe_render("GAME OVER", 48, (255, 255, 255))
            text_score = safe_render(f"SCORE: {self.player.score}", 24, (255, 255, 255))
            text_restart = safe_render("PRESS START / ENTER TO RESTART", 24, (255, 255, 255))

            if text_go and text_score and text_restart:
                screen.blit(text_go, (W // 2 - text_go.get_width() // 2, H // 2 - 40))
                screen.blit(text_score, (W // 2 - text_score.get_width() // 2, H // 2 + 10))
                screen.blit(text_restart, (W // 2 - text_restart.get_width() // 2, H // 2 + 60))
            else:
                draw_pixel_text(screen, "GAME OVER", W // 2, H // 2 - 40, scale=4, color=(255, 255, 255))
                draw_pixel_text(screen, f"SCORE: {self.player.score}", W // 2, H // 2 + 10, scale=2,
                                color=(255, 255, 255))
                draw_pixel_text(screen, "PRESS START TO RESTART", W // 2, H // 2 + 50, scale=1, color=(255, 255, 255))
            return

        if self.game_won:
            screen.fill((0, 0, 0))
            text_vic = safe_render("VICTORY WW", 48, (255, 255, 255))
            text_score = safe_render(f"SCORE: {self.player.score}", 24, (255, 255, 255))
            text_restart = safe_render("PRESS START TO PLAY AGAIN", 24, (255, 255, 255))

            if text_vic and text_score and text_restart:
                screen.blit(text_vic, (W // 2 - text_vic.get_width() // 2, H // 2 - 40))
                screen.blit(text_score, (W // 2 - text_score.get_width() // 2, H // 2 + 10))
                screen.blit(text_restart, (W // 2 - text_restart.get_width() // 2, H // 2 + 60))
            else:
                draw_pixel_text(screen, "VICTORY WW", W // 2, H // 2 - 40, scale=4, color=(255, 255, 255))
                draw_pixel_text(screen, f"SCORE: {self.player.score}", W // 2, H // 2 + 10, scale=2,
                                color=(255, 255, 255))
                draw_pixel_text(screen, "PRESS START TO PLAY AGAIN", W // 2, H // 2 + 50, scale=1,
                                color=(255, 255, 255))
            return

        screen.fill(BG_COLOR)
        self.maze.draw(screen, pygame)
        self.player.draw(screen, self.frame_count)
        for idx, ghost in enumerate(self.ghosts):
            ghost.draw(screen, self.frame_count, idx)

        score_text = safe_render(f"SCORE: {self.player.score}", 20, (255, 255, 255))
        if score_text:
            screen.blit(score_text, (10, H - 20))
        else:
            draw_pixel_text(screen, f"SCORE: {self.player.score}", 40, H - 18, scale=1, color=(255, 255, 255))

        for i in range(self.player.lives):
            lx = W - 20 - i * 16
            ly = H - 10
            pygame.draw.circle(screen, Y, (lx, ly), 6)
            pygame.draw.polygon(screen, BG_COLOR, [(lx, ly), (lx - 8, ly - 4), (lx - 8, ly + 4)])
