import pygame
from os.path import join as path_join

from assets.scripts.math_and_data.enviroment import WIDTH, HEIGHT


def render_fps(func):
    def wrapper(self, screen, clock):
        func(self, screen, clock)
        fps_label = self.fps_font.render(f"{format(round(clock.get_fps(), 1), '.1f')} fps", True,
                                         (255, 255, 255)).convert_alpha()
        screen.blit(fps_label, (WIDTH - fps_label.get_rect().w - 30, HEIGHT - fps_label.get_rect().h))

    return wrapper


class Scene:
    def __init__(self):
        self.fps_font = pygame.font.Font(path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 36)
        self.next = self

    def process_input(self, events) -> None:
        pass

    def update(self, deltatime) -> None:
        pass

    @render_fps
    def render(self, screen, clock) -> None:
        pass

    def switch_to_scene(self, next_scene) -> None:
        self.next = next_scene
