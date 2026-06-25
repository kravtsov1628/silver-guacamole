import pygame
from maze import Maze
from player import Player
from ghost import Ghost
from settings import *


class Game:
    def __init__(self):
        self.game_over = False
        self.maze=Maze()
        self.player=Player(9,8)
        self.ghosts = [
            Ghost(96, 96, R),
            Ghost(300, 55, (255, 105, 180)),
            Ghost(96, 256, (0, 255, 255)),
            Ghost(129, 200, (255, 165, 0))
        ]

    def update(self):
        self.player.input()
        self.player.update(self.maze)
        for ghost in self.ghosts:
            ghost.update(self.maze)
        if not self.game_over:
            self.player.input()
            self.player.update(self.maze)
            for ghost in self.ghosts:
                ghost.update(self.maze)
            self.coll()

    def draw(self,screen):
        screen.fill(B)
        self.maze.draw(screen,pygame)
        self.player.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)

    def coll(self):
        for ghost in self.ghosts:
            dx = self.player.x - ghost.x
            dy = self.player.y - ghost.y
            if dx * dx + dy * dy < 20 * 20:
                self.player.lives -= 1
                self.player.x = 9
                self.player.y = 8

                if self.player.lives <= 0:
                    self.game_over = True