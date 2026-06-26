import random
import pygame
from settings import T_SIZE


DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]


class Ghost:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.direction = random.choice(DIRECTIONS)
        self.color = color

    def update(self, maze):
        dr, dc = self.direction
        next_row = self.row + dr
        next_col = self.col + dc
        if not maze.is_free(next_col, next_row):
            self.choose_direction(maze)
            dr, dc = self.direction
            next_row = self.row + dr
            next_col = self.col + dc

        if maze.is_free(next_col, next_row):
            self.row = next_row
            self.col = next_col

    def choose_direction(self, maze):
        possible = []
        for dr, dc in DIRECTIONS:
            nr = self.row + dr
            nc = self.col + dc
            if maze.is_free(nc, nr):
                possible.append((dr, dc))
        reverse = (-self.direction[0], -self.direction[1])
        if reverse in possible and len(possible) > 1:
            possible.remove(reverse)
        self.direction = random.choice(possible)

    def draw(self, screen):
        x = self.col * T_SIZE + T_SIZE // 2
        y = self.row * T_SIZE + T_SIZE // 2
        pygame.draw.circle(
            screen,
            self.color,
            (x, y),
            T_SIZE // 2 - 3
        )