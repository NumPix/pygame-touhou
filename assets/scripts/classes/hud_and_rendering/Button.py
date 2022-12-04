import pygame

from assets.scripts.classes.SpriteSheet import SpriteSheet


class Button:
    def __init__(self, sprite_sheet, rect: pygame.Rect,
                 on_mouse_enter: callable = None, on_mouse_click: callable = None):

        if type(sprite_sheet) == SpriteSheet:

            self.default_sprite = sprite_sheet[0].image
            self.hovered_sprite = sprite_sheet[1].image
            self.pressed_sprite = sprite_sheet[2].image

        else:
            self.default_sprite = sprite_sheet[0]
            self.hovered_sprite = sprite_sheet[1]
            self.pressed_sprite = sprite_sheet[2]

        self.rect = rect

        self.hovered: bool = False
        self.pressed: bool = False

        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_click = on_mouse_click

    def draw(self, screen):
        sprite: pygame.Surface

        if self.pressed:
            if self.hovered:
                sprite = self.pressed_sprite
            else:
                sprite = self.default_sprite
        elif self.hovered:
            sprite = self.hovered_sprite
        else:
            sprite = self.default_sprite

        screen.blit(sprite, self.rect)

    def check_state(self, events: [pygame.event, ...]):
        cursor = pygame.mouse.get_pos()

        if self.rect.collidepoint(cursor):
            hovered = True
        else:
            hovered = False

        if not self.hovered and hovered:
            if self.on_mouse_enter:
                self.on_mouse_enter()

        self.hovered = hovered

        for evt in events:
            if evt.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                self.pressed = True
            if evt.type == pygame.MOUSEBUTTONUP and self.hovered:
                self.pressed = False
                if self.on_mouse_click:
                    self.on_mouse_click()
