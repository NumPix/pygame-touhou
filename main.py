import numpy
import pygame
from pygame.locals import *
from assets.scripts.classes.Player import Player
from assets.scripts.classes.Vector2 import Vector2

SIZE = WIDTH, HEIGHT = 1200, 800

clock = pygame.time.Clock()


def draw():
    screen.fill((0, 0, 0))
    player.update()

    bullet_group = pygame.sprite.RenderPlain()

    for bullet in player.bullets:
        on_screen = bullet.move()
        if not on_screen:
            player.bullets.remove(bullet)
        bullet_group.add(bullet.get_sprite())

    group = pygame.sprite.RenderPlain()
    group.add(player.get_sprite())

    group.draw(screen)
    bullet_group.draw(screen)
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

        move_direction = Vector2.zero()

        if pygame.key.get_pressed()[pygame.K_UP]:
            move_direction += Vector2.up()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            move_direction += Vector2.down()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            move_direction += Vector2.left()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            move_direction += Vector2.right()

        if pygame.key.get_pressed()[pygame.K_z]:
            player.shoot()

        player.move(move_direction)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            player.slow = True
        else:
            player.slow = False
