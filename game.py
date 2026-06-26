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
            Ghost(1, 1, (255, 0, 0)),
            Ghost(1, 18, (255, 105, 180)),
            Ghost(8, 1, (0, 255, 255)),
            Ghost(8, 18, (255, 165, 0))
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
        if (ghost.row == self.player.row and
                ghost.col == self.player.col):
            self.player.lives -= 1
            self.player.row = 8
            self.player.col = 9
            if self.player.lives <= 0:
                self.game_over = True