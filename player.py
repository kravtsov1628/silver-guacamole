import pygame
import math
import random
import script
from settings import *


class Particle:
    def __init__(self, x, y, vx, vy, color, size, max_life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = 0
        self.max_life = max_life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life += 1

    def draw(self, screen):
        ratio = self.life / self.max_life
        r = int(250 - 100 * ratio)
        g = int(204 - 150 * ratio)
        b = int(21 - 21 * ratio)
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(max(1, self.size)))


class Player:
    def __init__(self, col, row):
        # Grid coordinates
        self.col = col
        self.row = row
        self.pixel_x = col * T_SIZE
        self.pixel_y = row * T_SIZE
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.last_nonzero_direction = (1, 0)
        self.lives = 3
        self.score = 0
        self.speed = P_SPEED
        self.state = "alive"
        self.dying_timer = 0
        self.respawn_timer = 0
        self.particles = []

    def input(self):
        if self.state == "dying":
            return

        if script.pressed("LEFT"):
            self.next_direction = (-1, 0)
        elif script.pressed("RIGHT"):
            self.next_direction = (1, 0)
        elif script.pressed("UP"):
            self.next_direction = (0, -1)
        elif script.pressed("DOWN"):
            self.next_direction = (0, 1)

    def trigger_death(self, sfx_manager):
        self.state = "dying"
        self.dying_timer = 45
        self.direction = (0, 0)
        self.next_direction = (0, 0)

        self.particles = []
        px = self.pixel_x + T_SIZE // 2
        py = self.pixel_y + T_SIZE // 2
        for _ in range(35):
            angle = random.random() * math.pi * 2
            speed = 1.5 + random.random() * 3.5
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = 2 + random.random() * 4
            max_life = 30 + random.randint(0, 20)
            self.particles.append(Particle(px, py, vx, vy, Y, size, max_life))

        if sfx_manager:
            sfx_manager.play_death()

    def update(self, maze, sfx_manager=None):
        if self.state == "dying":
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.life < p.max_life]

            self.dying_timer -= 1
            if self.dying_timer <= 0:
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "game_over"
                    if sfx_manager:
                        sfx_manager.play_game_over()
                else:
                    # Respawn
                    self.col = 9
                    self.row = 8
                    self.pixel_x = 9 * T_SIZE
                    self.pixel_y = 8 * T_SIZE
                    self.direction = (0, 0)
                    self.next_direction = (0, 0)
                    self.state = "respawning"
                    self.respawn_timer = 120
                    if sfx_manager:
                        sfx_manager.start_bgm()
            return

        if self.state == "respawning":
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.state = "alive"

        if self.direction != (0, 0):
            self.last_nonzero_direction = self.direction

        if self.pixel_x % T_SIZE == 0 and self.pixel_y % T_SIZE == 0:
            self.col = self.pixel_x // T_SIZE
            self.row = self.pixel_y // T_SIZE

            points = maze.eat(self.col, self.row)
            self.score += points
            if points == 10:
                if sfx_manager:
                    sfx_manager.play_eat()
            elif points == 50:
                if sfx_manager:
                    sfx_manager.play_power_eat()

            nd_col, nd_row = self.next_direction
            if maze.is_free(self.col + nd_col, self.row + nd_row):
                self.direction = self.next_direction
            else:
                d_col, d_row = self.direction
                if not maze.is_free(self.col + d_col, self.row + d_row):
                    self.direction = (0, 0)

        d_col, d_row = self.direction
        self.pixel_x += d_col * self.speed
        self.pixel_y += d_row * self.speed

    def draw(self, screen, frame_count):
        if self.state == "dying":
            for p in self.particles:
                p.draw(screen)
            return

        if self.state == "respawning" and (self.respawn_timer // 6) % 2 != 0:
            return
        cx = self.pixel_x + T_SIZE // 2
        cy = self.pixel_y + T_SIZE // 2
        r = T_SIZE // 2 - 2
        pygame.draw.circle(screen, Y, (cx, cy), r)
        dc, dr = self.last_nonzero_direction
        theta = 0
        if dc == 1:
            theta = 0
        elif dc == -1:
            theta = math.pi
        elif dr == 1:
            theta = math.pi / 2
        elif dr == -1:
            theta = 3 * math.pi / 2

        is_moving = self.direction != (0, 0)
        chomp_speed = 0.35 if is_moving else 0.15
        mouth_open = abs(math.sin(frame_count * chomp_speed)) * 0.32 + 0.05
        x1 = cx + (r + 4) * math.cos(theta - mouth_open)
        y1 = cy + (r + 4) * math.sin(theta - mouth_open)
        x2 = cx + (r + 4) * math.cos(theta + mouth_open)
        y2 = cy + (r + 4) * math.sin(theta + mouth_open)
        pygame.draw.polygon(screen, BG_COLOR, [(cx, cy), (int(x1), int(y1)), (int(x2), int(y2))])
