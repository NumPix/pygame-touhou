import numpy
import pygame
from pygame.locals import *
from assets.scripts.classes.Player import Player
from assets.scripts.classes.Vector2 import Vector2

SIZE = WIDTH, HEIGHT = 1200, 800

clock = pygame.time.Clock()


def draw():
    screen.fill((0, 0, 0))

    player.next_sprite()

    group = pygame.sprite.RenderPlain()
    group.add(player.get_sprite())

    group.draw(screen)
    pygame.display.flip()

    clock.tick(60)


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)

    player = Player(0)

    while True:
        draw()

        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()

        if pygame.key.get_pressed()[pygame.K_UP]:
            player.move(Vector2.down())
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player.move(Vector2.up())
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.move(Vector2.left())
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.move(Vector2.right())

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            player.slow = True
        else:
            player.slow = False
