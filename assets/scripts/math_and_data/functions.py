import pygame


def clamp(value, min_v, max_v):
    return max(min_v, min(max_v, value))


def text_button_sprites(text: str, font: pygame.font.Font, default_color, hovered_color, pressed_color) -> [pygame.Surface, ...]:
    return [
            font.render(text, True, default_color).convert_alpha(),
            font.render(text, True, hovered_color).convert_alpha(),
            font.render(text, True, pressed_color).convert_alpha()
        ]


def scale_sprite(sprite: pygame.sprite.Sprite, scale: float = 1) -> pygame.sprite.Sprite:
    sprite.image = pygame.transform.scale(sprite.image, (sprite.rect.w * scale, sprite.rect.h * scale)).convert_alpha()
    print(sprite.image)
    sprite.rect = sprite.image.get_rect()
    return sprite
