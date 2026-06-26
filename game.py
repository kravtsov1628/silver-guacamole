import pygame
import script
from maze import Maze
from player import Player
from ghost import Ghost
from settings import *


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
                pygame.display.set_caption(f"Pacman - VICTORY! | SCORE: {self.player.score}")
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
            text_go = safe_render("GAME OVER", 48, (239, 68, 68))
            text_score = safe_render(f"SCORE: {self.player.score}", 24, (255, 255, 255))
            text_restart = safe_render("Press START / ENTER to restart", 24, (100, 116, 139))

            if text_go and text_score and text_restart:
                screen.blit(text_go, (W // 2 - text_go.get_width() // 2, H // 2 - 40))
                screen.blit(text_score, (W // 2 - text_score.get_width() // 2, H // 2 + 10))
                screen.blit(text_restart, (W // 2 - text_restart.get_width() // 2, H // 2 + 60))
            else:
                pygame.draw.rect(screen, (239, 68, 68), (W // 2 - 100, H // 2 - 30, 200, 60), 2)
            return

        if self.game_won:
            screen.fill((0, 0, 0))
            text_vic = safe_render("VICTORY WW", 48, (34, 197, 94))
            text_score = safe_render(f"SCORE: {self.player.score}", 24, (255, 255, 255))
            text_restart = safe_render("Press START / ENTER to play again", 24, (100, 116, 139))

            if text_vic and text_score and text_restart:
                screen.blit(text_vic, (W // 2 - text_vic.get_width() // 2, H // 2 - 40))
                screen.blit(text_score, (W // 2 - text_score.get_width() // 2, H // 2 + 10))
                screen.blit(text_restart, (W // 2 - text_restart.get_width() // 2, H // 2 + 60))
            else:
                pygame.draw.rect(screen, (34, 197, 94), (W // 2 - 100, H // 2 - 30, 200, 60), 2)
            return

        screen.fill(BG_COLOR)
        self.maze.draw(screen, pygame)
        self.player.draw(screen, self.frame_count)
        for idx, ghost in enumerate(self.ghosts):
            ghost.draw(screen, self.frame_count, idx)

        score_text = safe_render(f"SCORE: {self.player.score}", 20, (255, 255, 255))
        if score_text:
            screen.blit(score_text, (10, H - 20))

        for i in range(self.player.lives):
            lx = W - 20 - i * 16
            ly = H - 10
            pygame.draw.circle(screen, Y, (lx, ly), 6)
            pygame.draw.polygon(screen, BG_COLOR, [(lx, ly), (lx - 8, ly - 4), (lx - 8, ly + 4)])
