import numpy as np
import pygame
from pygame.locals import *
import json
from os.path import join as path_join

from assets.scripts.classes.game_logic.BulletData import BulletData
from assets.scripts.classes.game_logic.Collider import Collider
from assets.scripts.classes.game_logic.Enemy import Enemy
from assets.scripts.classes.game_logic.Item import *
from assets.scripts.classes.game_logic.Player import Player
from assets.scripts.classes.hud_and_rendering.Scene import Scene, render_fps
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.classes.game_logic.AttackFunctions import AttackFunctions

from assets.scripts.math_and_data.enviroment import *

from PIL import Image


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))
        self.delta_time = 0.001

        music_module.play_music("08.-Voile_-the-Magic-Library_1.wav")

        self.background = Image.open(path_join("assets", "sprites", "backgrounds", "background.png")).convert("RGBA")
        self.background.paste(Image.new("RGBA", (GAME_ZONE[2], GAME_ZONE[3]), (255, 255, 255, 0)),
                              (GAME_ZONE[0], GAME_ZONE[1]))
        self.bg = pygame.sprite.Sprite()
        self.bg.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.bg.image = pygame.image.fromstring(self.background.tobytes(), self.background.size, self.background.mode).convert_alpha()

        self.font = pygame.font.Font(path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 36)

        self.player = Player(0, self, 1)

        self.enemy_bullets = []
        self.items = []
        self.bullet_cleaner = None

        self.bullet_group = pygame.sprite.RenderPlain()
        self.item_group = pygame.sprite.RenderPlain()
        self.hud_group = pygame.sprite.RenderPlain()
        self.entity_group = pygame.sprite.RenderPlain()

        self.time = 0
        self.level = json.load(open(path_join("assets", "levels", "touhou", "level_1.json")))
        self.level_enemies = sorted(self.level["enemies"], key=lambda enemy: enemy["time"])
        self.enemy_count = 0

        self.enemies = []

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

    def update(self, delta_time):
        self.delta_time = delta_time
        self.time += delta_time

        if self.level_enemies and self.enemy_count < len(self.level_enemies):
            if self.time >= self.level_enemies[self.enemy_count]["time"]:
                enemy_data = self.level_enemies[self.enemy_count]
                enemy = Enemy(
                    position=Vector2(GAME_ZONE[0], GAME_ZONE[1]) + Vector2(*enemy_data["start_position"]),
                    trajectory=list(map(np.array, [enemy_data["start_position"]]+ enemy_data["trajectory"])),
                    speed=enemy_data["speed"],
                    sprite_sheet=SpriteSheet(path_join(*enemy_data["sprite"]["path"])).crop(enemy_data["sprite"]["size"]),
                    collider=Collider(enemy_data["collider"]["radius"], offset=Vector2(*enemy_data["collider"]["offset"])),
                    hp=enemy_data["hp"],
                    attack_data=[(*attack[:3], (path_join(*attack[3][0]), attack[3][1], attack[3][2], attack[3][3], Vector2(*attack[3][4])), *attack[4:]) for attack in enemy_data["attacks"]],
                    drop=(enemy_data["drop"]["list"], enemy_data["drop"]["list"]),
                    bullet_pool=self.enemy_bullets,
                    scene=self
                )

                attack_data = []
                for i in range(len(enemy.attack_data)):
                    if enemy.attack_data[i][0] == "wide_ring":
                        _, bul_num, ring_num, bul_data, spd, s_time, delay, a_speed, d_angle, rand_cnt = \
                        enemy.attack_data[i]
                        attack_data.extend(
                        AttackFunctions.wide_ring
                            (
                                number_of_bullets=bul_num,
                                number_of_rings=ring_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                delta_angle=d_angle,
                                rand_center=rand_cnt
                            )
                        )
                    elif enemy.attack_data[i][0] == "long_random":
                        _, bul_num, rand_num, bul_data, spd, s_time, delay, a_speed, rand_cnt = \
                        enemy.attack_data[i]
                        attack_data.extend(
                        AttackFunctions.long_random
                            (
                                number_of_bullets=bul_num,
                                number_of_randoms=rand_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                rand_center=rand_cnt
                            )
                        )
                    elif enemy.attack_data[i][0] == "wide_cone":
                        _, bul_num, cone_num, bul_data, angle, spd, d_angle, s_time, delay, a_speed = enemy.attack_data[i]
                        attack_data.extend(
                            AttackFunctions.wide_cone(
                                number_of_bullets=bul_num,
                                number_of_cones=cone_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                angle=angle,
                                speed=spd,
                                delta_angle=d_angle,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                player=self.player,
                                enemy=enemy
                            )
                        )
                    enemy.attack_data = attack_data

                self.enemies.append(enemy)
                self.enemy_count += 1

        for enemy in self.enemies:
            enemy.update()
            enemy.move()

        for bullet in self.player.bullets:
            on_screen = bullet.move(delta_time)
            if not on_screen:
                self.player.bullets.remove(bullet)
                del bullet

        for item in self.items:
            on_screen = item.move(delta_time, self.player)
            if not on_screen:
                self.items.remove(item)
                del item

        if self.bullet_cleaner:
            self.bullet_cleaner.update(self.enemy_bullets, self, delta_time)
            if self.bullet_cleaner.kill:
                del self.bullet_cleaner
                self.bullet_cleaner = None

        for bullet in self.enemy_bullets:
            on_screen = bullet.move(delta_time)
            if not on_screen:
                self.enemy_bullets.remove(bullet)
                del bullet

        self.player.update()

    @render_fps
    def render(self, screen, clock):
        screen.fill((0, 0, 0), rect=GAME_ZONE)

        for bullet in self.player.bullets:
            self.bullet_group.add(bullet.get_sprite())

        for bullet in self.enemy_bullets:
            self.bullet_group.add(bullet.get_sprite())

        for item in self.items:
            self.item_group.add(item.get_sprite())

        self.hud_group.add(self.bg)

        high_score = sorted(db_module.get_leaderboard(), key=lambda x: x[1])[-1][1] if len(db_module.get_leaderboard()) > 0 else 0

        hi_score_label = self.font.render(f"HiScore:    {format(high_score if high_score > self.player.points else self.player.points, '09d')}", True, (255, 255, 255)).convert_alpha()

        score_label = self.font.render(f"Score:    {format(self.player.points, '09d')}", True, (255, 255, 255)).convert_alpha()

        power_label = self.font.render(f"Power:    {format(round(self.player.power, 2), '.2f')} / 4.00", True,
                                       (255, 255, 255)).convert_alpha()

        hp_label = self.font.render(f"Player:   {'★' * self.player.hp}", True, (255, 255, 255)).convert_alpha()

        player_sprite = self.player.get_sprite()
        if self.player.reviving and self.player.invincibility_timer % 40 > 30:
            player_sprite.image.set_alpha(170)

        self.entity_group.add(player_sprite)

        for enemy in self.enemies:
            self.entity_group.add(enemy.get_sprite())

        self.entity_group.draw(screen)
        self.item_group.draw(screen)
        self.bullet_group.draw(screen)

        if self.bullet_cleaner:
            screen.blit(self.bullet_cleaner.get_sprite(), (self.bullet_cleaner.collider.position - self.bullet_cleaner.collider.radius).to_tuple())

        pygame.draw.circle(screen, (255, 0, 0), self.player.collider.position.to_tuple(), self.player.collider.radius)

        self.hud_group.draw(screen)

        screen.blit(hi_score_label, (GAME_ZONE[0] + GAME_ZONE[2] + 13, 160))
        screen.blit(score_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 210))
        screen.blit(hp_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 280))
        screen.blit(power_label, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 330))

        self.entity_group.empty()
        self.item_group.empty()
        self.bullet_group.empty()
        self.bullet_group.empty()
        self.hud_group.empty()
