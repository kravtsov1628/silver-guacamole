import pygame
import script
from settings import *
from game import Game


pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
except Exception:
    pass

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pacman Edition")
clock = pygame.time.Clock()
sfx_manager = script.SoundManager()
game = Game(sfx_manager)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()
    game.draw(screen)
    pygame.display.flip()

sfx_manager.stop_bgm()
pygame.quit()
script.cleanup()
