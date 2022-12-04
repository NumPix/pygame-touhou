import pygame.image
from pygame.locals import *

from assets.scripts.scenes.GameScene import GameScene
from assets.scripts.math_and_data.enviroment import *
from assets.scripts.classes.hud_and_rendering.Scene import Scene
from assets.scripts.classes.hud_and_rendering.Button import Button


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.sprite.Sprite()
        self.background.rect = (0, 0, WIDTH, HEIGHT)
        self.background.image = pygame.image.load("assets/sprites/backgrounds/title_screen_wallpaper.jpg").convert_alpha()

        self.font = pygame.font.Font('assets/fonts/DFPPOPCorn-W12.ttf', 45)
        play_button_sprites = [
            self.font.render("Play", True, (255, 255, 255)).convert_alpha(),
            self.font.render("Play", True, (100, 100, 100)).convert_alpha(),
            self.font.render("Play", True, (100, 100, 100)).convert_alpha()
        ]

        play_button_size = play_button_sprites[0].get_size()

        self.play_button = Button(play_button_sprites, pygame.Rect(1000, 100, play_button_size[0], play_button_size[1]),
                                  on_mouse_click=(lambda: self.switch_to_scene(GameScene())))

    def render(self, screen, clock):
        background_group = pygame.sprite.RenderPlain()
        background_group.add(self.background)

        background_group.draw(screen)

        self.play_button.draw(screen)

    def process_input(self, events):
        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

        self.play_button.check_state(events)
