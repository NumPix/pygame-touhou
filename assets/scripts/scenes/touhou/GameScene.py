import numpy as np
import pygame
from pygame.locals import *

from assets.scripts.classes.game_logic.touhou.Collider import Collider
from assets.scripts.classes.game_logic.touhou.Enemy import Enemy
from assets.scripts.classes.game_logic.touhou.Player import Player
from assets.scripts.classes.hud_and_rendering.Scene import Scene
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.math_and_data.enviroment import *

from PIL import Image

from assets.scripts.math_and_data.functions import scale_sprite


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))

        self.background = Image.open("assets/sprites/touhou/backgrounds/background.png").convert("RGBA")
        self.background.paste(Image.new("RGBA", (GAME_ZONE[2], GAME_ZONE[3]), (255, 255, 255, 0)),
                              (GAME_ZONE[0], GAME_ZONE[1]))

        self.bg = pygame.sprite.Sprite()
        self.bg.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.bg.image = pygame.image.fromstring(self.background.tobytes(), self.background.size, self.background.mode)

        self.font = pygame.font.Font('assets/fonts/DFPPOPCorn-W12.ttf', 30)

        self.player = Player(0)

        self.enemy = Enemy(Vector2(GAME_ZONE[0], GAME_ZONE[1]),
                           [np.array([250, 0]), np.array([100, 300]), np.array([0, 400]), np.array([550, 300]), np.array([250, 0])],
                           SpriteSheet("assets/sprites/touhou/entities/fairy_0.png").crop((24, 19)),
                           Collider(20),
                           1000, [], [],
                           self.player)

    def process_input(self, events):
        for evt in events:
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
            self.player.shoot()

        self.player.move(move_direction)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.player.slow = True
        else:
            self.player.slow = False

    def update(self):
        self.player.update()
        self.enemy.move()
        self.enemy.update()
        if not self.enemy.check_alive():
            self.enemy.position = Vector2(-100, 100)

    def render(self, screen, clock):
        screen.fill((0, 0, 0), rect=GAME_ZONE)
        bullet_group = pygame.sprite.RenderPlain()
        hud_group = pygame.sprite.RenderPlain()
        player_group = pygame.sprite.RenderPlain()

        for bullet in self.player.bullets:
            on_screen = bullet.move()
            if not on_screen:
                self.player.bullets.remove(bullet)
            bullet_group.add(bullet.get_sprite())

        hud_group.add(self.bg)

        fps_label = self.font.render(f"{format(round(clock.get_fps(), 1), '.1f')} fps", True,
                                     (255, 255, 255)).convert_alpha()
        power_label = self.font.render(f"power:  {format(round(self.player.power, 2), '.2f')} / 4.00", True,
                                       (255, 255, 255)).convert_alpha()

        player_group.add(self.player.get_sprite())
        player_group.add(self.enemy.get_sprite())

        player_group.draw(screen)
        bullet_group.draw(screen)
        hud_group.draw(screen)
        screen.blit(fps_label, (WIDTH - fps_label.get_rect().w - 25, HEIGHT - fps_label.get_rect().h))
        screen.blit(power_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 300))
