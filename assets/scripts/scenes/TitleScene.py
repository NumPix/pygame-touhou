import pygame.image
import time
from pygame.locals import *

from os.path import join as path_join

from assets.scripts.classes.hud_and_rendering.SelectButtonMatrix import SelectButtonMatrix
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.math_and_data.enviroment import *
from assets.scripts.classes.hud_and_rendering.Scene import Scene, render_fps


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        music_module.play_music("01.-A-Dream-that-is-more-Scarlet-than-Red_1.wav")

        self.background = pygame.sprite.Sprite()
        self.background.rect = (0, 0, WIDTH, HEIGHT)
        self.background.image = pygame.image.load(
            path_join("assets", "sprites", "backgrounds", "title_screen_wallpaper.jpg")
        ).convert_alpha()

        self.font = pygame.font.Font(path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 45)

        self.matrix = [[["Start", self.switch_to_game]], [["Score", self.switch_to_scoreboard]], [["Quit", self.quit]]]
        self.ButtonMatrix = SelectButtonMatrix(Vector2(100, 100), self.matrix, self.font, (100, 100, 100), (255, 50, 40))

    @render_fps
    def render(self, screen, clock):
        background_group = pygame.sprite.RenderPlain()
        background_group.add(self.background)

        background_group.draw(screen)

        self.ButtonMatrix.draw(screen)

    def process_input(self, events):
        self.ButtonMatrix.handle_events(events)

        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

    def switch_to_game(self):
        from assets.scripts.scenes.GameScene import GameScene
        self.switch_to_scene(GameScene())

    def switch_to_scoreboard(self):
        from assets.scripts.scenes.ScoreboardScene import ScoreboardScene
        self.switch_to_scene(ScoreboardScene())

    def quit(self):
        music_module.sounds[0](.1)
        time.sleep(.3)
        pygame.quit()

