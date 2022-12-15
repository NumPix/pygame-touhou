import numpy as np
import pygame
from pygame.locals import *

from assets.scripts.classes.game_logic.touhou.BulletData import BulletData
from assets.scripts.classes.game_logic.touhou.Collider import Collider
from assets.scripts.classes.game_logic.touhou.Enemy import Enemy
from assets.scripts.classes.game_logic.touhou.Player import Player
from assets.scripts.classes.hud_and_rendering.Scene import Scene
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.classes.game_logic.touhou.AttackFunctions import AttackFunctions

from assets.scripts.math_and_data.enviroment import *

from PIL import Image


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

        self.player = Player(0, self)

        self.enemy_bullets = []

        self.bullet_group = pygame.sprite.RenderPlain()
        self.hud_group = pygame.sprite.RenderPlain()
        self.entity_group = pygame.sprite.RenderPlain()

        self.enemies = [Enemy(position=Vector2(GAME_ZONE[0], GAME_ZONE[1]),
                              trajectory=[np.array([0, 0]), np.array([300, 0]), np.array([0, 400]), np.array([550, 300]), np.array([550, 0])],
                              speed = .4,
                              sprite_sheet= SpriteSheet("assets/sprites/touhou/entities/fairy_0.png").crop((24, 19)),
                              collider=Collider(10, offset=Vector2.down() * 10),
                              hp=50,
                              attack_data=[(lambda: AttackFunctions.ring(self.enemies[0].position,
                                                                         72,
                                                                         BulletData(SpriteSheet("assets/sprites/touhou/bullets/bullet_0.png").crop((16, 16)),
                                                                                    Collider(8)),
                                                                         3
                                                                         ),
                                            1),
                                           (lambda: AttackFunctions.ring(self.enemies[0].position,
                                                                         72,
                                                                         BulletData(SpriteSheet(
                                                                             "assets/sprites/touhou/bullets/bullet_0.png").crop(
                                                                             (16, 16)),
                                                                                    Collider(8)),
                                                                         3
                                                                         ),
                                            1.1),
                                           (lambda: AttackFunctions.ring(self.enemies[0].position,
                                                                         72,
                                                                         BulletData(SpriteSheet(
                                                                             "assets/sprites/touhou/bullets/bullet_0.png").crop(
                                                                             (16, 16)),
                                                                                    Collider(8)),
                                                                         3
                                                                         ),
                                            1.2)
                                           ],
                              bullet_pool=self.enemy_bullets,
                              scene=self),
                        ]


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
        for enemy in self.enemies:
            enemy.update()
            enemy.move()

        for bullet in self.player.bullets:
            on_screen = bullet.move()
            if not on_screen:
                self.player.bullets.remove(bullet)
                del bullet

        for bullet in self.enemy_bullets:
            on_screen = bullet.move()
            if not on_screen:
                self.enemy_bullets.remove(bullet)
                del bullet

        self.player.update()

    def render(self, screen, clock):
        screen.fill((0, 0, 0), rect=GAME_ZONE)

        for bullet in self.player.bullets:
            self.bullet_group.add(bullet.get_sprite())

        for bullet in self.enemy_bullets:
            self.bullet_group.add(bullet.get_sprite())

        self.hud_group.add(self.bg)

        fps_label = self.font.render(f"{format(round(clock.get_fps(), 1), '.1f')} fps", True,
                                     (255, 255, 255)).convert_alpha()
        power_label = self.font.render(f"power:  {format(round(self.player.power, 2), '.2f')} / 4.00", True,
                                       (255, 255, 255)).convert_alpha()

        self.entity_group.add(self.player.get_sprite())

        for enemy in self.enemies:
            self.entity_group.add(enemy.get_sprite())

        self.entity_group.draw(screen)
        self.bullet_group.draw(screen)
        self.hud_group.draw(screen)
        screen.blit(fps_label, (WIDTH - fps_label.get_rect().w - 25, HEIGHT - fps_label.get_rect().h))
        screen.blit(power_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 300))

        self.entity_group.empty()
        self.bullet_group.empty()
        self.bullet_group.empty()


        ## Draw hitboxes

        #for bullet in self.enemy_bullets:
            #pygame.draw.circle(screen, (255, 0, 0), bullet.collider.position.to_tuple(), bullet.collider.radius)

        pygame.draw.circle(screen, (255, 0, 0), self.player.collider.position.to_tuple(), self.player.collider.radius)

        #for enemy in self.enemies:
        #    pygame.draw.circle(screen, (0, 255, 0), enemy.collider.position.to_tuple(), enemy.collider.radius)
