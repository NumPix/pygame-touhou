import pygame

from assets.scripts.math_and_data.functions import text_button_sprites


class SelectButton:
    def __init__(self, text, default_color: (int, int, int), selected_color: (int, int, int), font, rect, on_trigger: callable = None):

        self.default_sprite: pygame.Surface
        self.selected_sprite: pygame.Surface

        self.default_sprite, self.selected_sprite = text_button_sprites(text, font, default_color, selected_color)

        self.rect: pygame.Rect = rect
        self.trigger = on_trigger
        self.selected = False

    def draw(self, screen) -> None:
        image: pygame.Surface

        if self.selected:
            image = pygame.transform.scale(self.selected_sprite, tuple(map(lambda x: x * 1.15, self.selected_sprite.get_size())))
        else:
            image = self.default_sprite

        screen.blit(image, self.rect)