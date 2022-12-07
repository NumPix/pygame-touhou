import pygame
from pygame.locals import *

from assets.scripts.classes.hud_and_rendering.Button import Button
from assets.scripts.classes.hud_and_rendering.Scene import Scene
from assets.scripts.math_and_data.functions import text_button_sprites


class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font('assets/fonts/DFPPOPCorn-W12.ttf', 45)

        touhou_button_sprites = text_button_sprites("Touhou", self.font, (255, 255, 255), (100, 100, 100),
                                                    (100, 100, 100))

        another_button_sprites = text_button_sprites("Another game", self.font, (255, 255, 255), (100, 100, 100),
                                                     (100, 100, 100))

        touhou_button_size = touhou_button_sprites[0].get_size()
        another_button_size = another_button_sprites[0].get_size()

        self.play_touhou_button = Button(touhou_button_sprites,
                                         pygame.Rect(100, 200, touhou_button_size[0], touhou_button_size[1]),
                                         on_mouse_click=self.switch_to_touhou)

        self.play_another_game_button = Button(another_button_sprites,
                                               pygame.Rect(100, 300, another_button_size[0], another_button_size[1]),
                                               on_mouse_click=self.switch_to_another_game)

    def render(self, screen: pygame.Surface, clock):
        screen.fill((80, 80, 100))

        self.play_touhou_button.draw(screen)
        self.play_another_game_button.draw(screen)

    def process_input(self, events):
        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

        self.play_touhou_button.check_state(events)
        self.play_another_game_button.check_state(events)

    def switch_to_touhou(self):
        import assets.scripts.scenes.touhou.TitleScene as thTitleScene
        self.switch_to_scene(thTitleScene.TitleScene())

    def switch_to_another_game(self):
        import assets.scripts.scenes.another_game.TitleScene as agTitleScene
        self.switch_to_scene(agTitleScene.TitleScene())
