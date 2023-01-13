import pygame
from pygame.locals import *

from assets.scripts.math_and_data.enviroment import *

pygame.init()

pygame.mixer.pre_init(44100, -16, 32, 512)
pygame.mixer.init()


screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)
clock = pygame.time.Clock()

from assets.scripts.scenes.TitleScene import TitleScene
active_scene = TitleScene()

ticksLastFrame = pygame.time.get_ticks()

delta_time = 1 / FPS

while active_scene is not None:
    active_scene.process_input(pygame.event.get())
    active_scene.update(delta_time)
    active_scene.render(screen, clock)

    active_scene = active_scene.next

    pygame.display.flip()
    delta_time = clock.tick(FPS) / 1000


db_module.close()

