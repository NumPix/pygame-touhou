import pygame
from pygame.locals import *

from assets.scripts.classes.Player import Player
from assets.scripts.classes.Vector2 import Vector2

from dotenv import load_dotenv
import os

from PIL import Image

clock = pygame.time.Clock()
load_dotenv(".env")

WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))
SIZE = WIDTH, HEIGHT
GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))

background = Image.open("assets/sprites/background.png").convert("RGBA")
background.paste(Image.new("RGBA", (GAME_ZONE[2], GAME_ZONE[3]), (255, 255, 255, 0)), (GAME_ZONE[0], GAME_ZONE[1]))

bg = pygame.sprite.Sprite()
bg.rect = Rect(0, 0, WIDTH, HEIGHT)
bg.image = pygame.image.fromstring(background.tobytes(), background.size, background.mode)

pygame.font.init()

font = pygame.font.Font('assets/fonts/DFPPOPCorn-W12.ttf', 30)


def draw():
    screen.fill((0, 0, 0), rect=GAME_ZONE)
    player.update()

    bullet_group = pygame.sprite.RenderPlain()

    for bullet in player.bullets:
        on_screen = bullet.move()
        if not on_screen:
            player.bullets.remove(bullet)
        bullet_group.add(bullet.get_sprite())

    hud_group = pygame.sprite.RenderPlain()
    hud_group.add(bg)

    fps_label = font.render(str(round(clock.get_fps(), 1)), True, (255, 255, 255))
    power_label = font.render(f"power:  {round(player.power, 2)} / 4.00", True, (255, 255, 255))

    player_group = pygame.sprite.RenderPlain()
    player_group.add(player.get_sprite())

    player_group.draw(screen)
    bullet_group.draw(screen)
    hud_group.draw(screen)
    screen.blit(fps_label, (WIDTH - fps_label.get_rect().w, HEIGHT - fps_label.get_rect().h))
    screen.blit(power_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 300))

    pygame.display.flip()

    clock.tick(60)


def check_inputs():
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


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)

    player = Player(0)

    while True:
        draw()
        check_inputs()
