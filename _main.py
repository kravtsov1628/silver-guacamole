import pygame
import script
from settings import *
from game import Game


pygame.init()
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("PM")
clock=pygame.time.Clock()
game=Game()
running=True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    game.update()
    game.draw(screen)
    pygame.display.flip()

pygame.quit()
script.cleanup()