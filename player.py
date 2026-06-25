import pygame
import script
from settings import *


class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.direction = (0, 0)
        self.lives = 3
        self.score = 0

    def input(self):
        if script.pressed("LEFT"):
            self.direction = (-1, 0)
        elif script.pressed("RIGHT"):
            self.direction = (1, 0)
        elif script.pressed("UP"):
            self.direction = (0, -1)
        elif script.pressed("DOWN"):
            self.direction = (0, 1)

    def update(self, maze):
        dx, dy = self.direction
        next_col = self.x + dx
        next_row = self.y + dy
        if maze.is_free(next_col, next_row):
            self.x = next_col
            self.y = next_row
            self.score += maze.eat(next_col, next_row)

    def is_free(self, col, row):
        if row < 0:
            return False
        if row >= len(self.map):
            return False
        if col < 0:
            return False
        if col >= len(self.map[row]):
            return False
        return self.map[row][col] != "#"

    def draw(self,screen):
        x = self.x * T_SIZE + T_SIZE // 2
        y = self.y * T_SIZE + T_SIZE // 2

        pygame.draw.circle(
            screen,
            Y,
            (x, y),
            T_SIZE // 2 - 2
        )