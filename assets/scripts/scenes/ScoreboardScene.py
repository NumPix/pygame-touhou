import pygame
import datetime
from pygame.locals import *
from os.path import join as path_join

from assets.scripts.classes.game_logic.Player import Player
from assets.scripts.classes.hud_and_rendering.Scene import Scene, render_fps
from assets.scripts.classes.hud_and_rendering.ScoreboardLine import ScoreboardLine
from assets.scripts.classes.hud_and_rendering.SelectButtonMatrix import SelectButtonMatrix
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.math_and_data.enviroment import WIDTH, HEIGHT, db_module
from assets.scripts.math_and_data.functions import clamp


class ScoreboardScene(Scene):
    def __init__(self, player: Player = None):
        super().__init__()

        self.font = pygame.font.Font(path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 24)
        self.player = player

        self.leaderboard = list(map(lambda x: ScoreboardLine(*x), db_module.get_leaderboard()))
        self.leaderboard.sort(reverse=True)

        if player is not None:

            self.cursor = 0
            self.MAX_NAME_LENGTH = 8

            self.statistics = ScoreboardLine(" " * self.MAX_NAME_LENGTH, self.player.points, datetime.date.today().strftime("%d/%m/%y"), round(self.player.slowRate.tan(), 2), True)

            if len(self.leaderboard) < 10 or self.statistics > self.leaderboard[-1]:
                self.leaderboard.append(self.statistics)
                self.leaderboard.sort(reverse=True)
                if len(self.leaderboard) > 10:
                    self.leaderboard.pop(-1)
            else:
                self.switch_to_menu()


            self.name = " " * self.MAX_NAME_LENGTH

            self.matrix = [
                [[char, lambda char=char: self.type_letter(char)] for char in "ABCDEFGHIJKLMNOP"],
                [[char, lambda char=char: self.type_letter(char)] for char in "QRSTUVWXYZ.,:;_@"],
                [[char, lambda char=char: self.type_letter(char)] for char in "abcdefghijklmnop"],
                [[char, lambda char=char: self.type_letter(char)] for char in "qrstuvwxyz+-/*=%"],
                [[char, lambda char=char: self.type_letter(char)] for char in "0123456789#!?\'\"$"],
                [[char, lambda char=char: self.type_letter(char)] for char in "(){}[]<>&|~^  "] + [["←", self.delete_letter]] + [["End", self.save]]
            ]
            self.keyboard = SelectButtonMatrix(Vector2(WIDTH // 2 - 250, HEIGHT // 2 + 150), self.matrix, self.font, (100, 100, 100), (255, 50, 40), padding=Vector2(30, 35))
            self.keyboard.cursor = Vector2(15, 5)

    def type_letter(self, char: str):
        if self.cursor == self.MAX_NAME_LENGTH:
            self.save()
        self.name = list(self.name)
        self.name[self.cursor] = char
        self.name = ''.join(self.name)
        self.cursor += 1

    def delete_letter(self):
        self.name = list(self.name)

        if self.cursor == self.MAX_NAME_LENGTH:
            self.cursor -= 1

        if self.name[self.cursor] != " ":
            self.name.pop(self.cursor)
            self.name.append(" ")
        else:
            self.cursor = clamp(self.cursor - 1, 0, self.MAX_NAME_LENGTH)
            self.name.pop(self.cursor)
            self.name.append(" ")

        self.name = "{:8}".format(''.join(self.name))

    def process_input(self, events):
        if self.player is not None:
            self.keyboard.handle_events(events)

        for evt in events:
            if evt.type == QUIT:
                pygame.quit()
            if evt.type == pygame.KEYDOWN:
                if evt.key == K_x:
                    if self.player is not None:
                        self.delete_letter()
                    else:
                        self.switch_to_menu()

    def text_render(self, screen, text: str, position: Vector2, padding: int, color=(255, 255, 255)):
        for i in range(len(text)):
            letter = text[i]
            letter_label = self.font.render(letter, True, color).convert_alpha()
            screen.blit(letter_label, (position + Vector2(padding, 0) * i).to_tuple())

    @render_fps
    def render(self, screen, clock):
        screen.fill((0, 0, 0))

        self.text_render(screen, "No   Name            Score       Date      Slow", Vector2(100, 60), 20)

        for i in range(len(self.leaderboard)):
            line = self.leaderboard[i]
            if not line.player:
                self.text_render(screen, "{:2}   ".format(i + 1) + str(line), Vector2(100, 100 + i * 30), 20, (255, 150, 150))
            else:
                self.text_render(screen, "     " + " " * clamp(self.cursor, 0, self.MAX_NAME_LENGTH - 1) + "_" + " " * (self.MAX_NAME_LENGTH - clamp(self.cursor, 0, self.MAX_NAME_LENGTH - 1) - 1),  Vector2(100, 100 + i * 30), 20)
                self.text_render(screen, "{:2}   ".format(i + 1) + (self.name if self.name != " " * self.MAX_NAME_LENGTH else "_" * self.MAX_NAME_LENGTH) + str(line)[8:],  Vector2(100, 100 + i * 30), 20)

        if self.player is not None:
            self.keyboard.draw(screen)

    def switch_to_menu(self):
        from assets.scripts.scenes.TitleScene import TitleScene
        self.switch_to_scene(TitleScene())

    def save(self):
        self.statistics.name = self.name
        if self.statistics.name != "        ":
            db_module.add_to_leaderboard(self.statistics)
        self.switch_to_menu()