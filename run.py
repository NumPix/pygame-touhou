import pygame
from pygame.locals import *
from assets.scripts.math_and_data.enviroment import *
import asyncio

pygame.init()
screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)
clock = pygame.time.Clock()

from assets.scripts.scenes import MenuScene

active_scene = MenuScene.MenuScene()

ticksLastFrame = pygame.time.get_ticks()

while active_scene is not None:
    t = pygame.time.get_ticks()
    delta_time = (t - ticksLastFrame) / 1000

    active_scene.process_input(pygame.event.get())
    active_scene.update(delta_time)
    active_scene.render(screen, clock)

    active_scene = active_scene.next

    pygame.display.flip()
    clock.tick(FPS)

    ticksLastFrame = t
