import os
from settings import *


class Maze:
    def __init__(self):
        self.map = []
        map_path = "bin/maps/the_diary_of_Jane.txt"

        if os.path.exists(map_path):
            with open(map_path) as f:
                for line in f:
                    stripped = line.strip()
                    if stripped:
                        self.map.append(list(stripped))

    def draw(self, screen, pygame_module):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                rect = pygame_module.Rect(
                    x * T_SIZE,
                    y * T_SIZE,
                    T_SIZE,
                    T_SIZE
                )
                if tile == "#":
                    pygame_module.draw.rect(screen, (10, 25, 100), rect)
                    pygame_module.draw.rect(screen, (30, 80, 250), rect, 1)
                elif tile == ".":
                    pygame_module.draw.circle(
                        screen,
                        WH,
                        rect.center,
                        3
                    )
                elif tile == "o":
                    pygame_module.draw.circle(
                        screen,
                        WH,
                        rect.center,
                        6
                    )

    def is_free(self, col, row):
        if row < 0 or row >= len(self.map):
            return False
        if col < 0 or col >= len(self.map[row]):
            return False
        return self.map[row][col] != "#"

    def eat(self, col, row):
        if row < 0 or row >= len(self.map) or col < 0 or col >= len(self.map[row]):
            return 0
        tile = self.map[row][col]
        if tile == ".":
            self.map[row][col] = " "
            return 10
        elif tile == "o":
            self.map[row][col] = " "
            return 50
        return 0
