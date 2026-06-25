from settings import *


class Maze:
    def __init__(self):
        self.map = []
        with open("bin/maps/the_diary_of_Jane.txt") as f:
            for _ in f:
                self.map.append(list(_.strip()))

    def draw(self, screen, pygame):
        for y,r in enumerate(self.map):
            for x,t in enumerate(r):
                rect = pygame.Rect(
                    x*T_SIZE,
                    y*T_SIZE,
                    T_SIZE,
                    T_SIZE
                )
                if t == "#":
                    pygame.draw.rect(screen,BL,rect)
                elif t == ".":
                    pygame.draw.circle(
                        screen,
                        WH,
                        rect.center,
                        3
                    )
                elif t == "o":
                    pygame.draw.circle(
                        screen,
                        WH,
                        rect.center,
                        7
                    )

    def walls(self, x, y):
        if x < 0:
            return False
        if x >= len(self.map):
            return False
        if y < 0:
            return False
        if y >= len(self.map[x]):
            return False
        return self.map[x][y] != "#"

    def eat(self, x, y):
        col = x
        row = y
        if self.map[row][col] == ".":
            self.map[row][col] = " "
            return 10
        if self.map[row][col] == "o":
            self.map[row][col] = " "
            return 50
        return 0