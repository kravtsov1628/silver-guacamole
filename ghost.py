import random
import pygame
from settings import *


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = G_SPEED
        self.dy = 0
        self.color = color

    def update(self, maze):
        new_x = self.x + self.dx
        new_y = self.y + self.dy
        if not maze.walls(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            self.change_direction()

    def change_direction(self):
        dirs = [
            (G_SPEED,0),
            (-G_SPEED,0),
            (0,G_SPEED),
            (0,-G_SPEED)
        ]
        self.dx,self.dy = random.choice(dirs)

    def draw(self,screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x),int(self.y)),
            12
        )