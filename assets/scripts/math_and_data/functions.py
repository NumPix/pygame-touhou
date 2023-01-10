import pygame


def clamp(value, min_v, max_v):
    return max(min_v, min(max_v, value))


def text_button_sprites(text: str, font: pygame.font.Font, default_color, selected_color) -> [pygame.Surface, ...]:
    return [
        font.render(text, True, default_color).convert_alpha(),
        font.render(text, True, selected_color).convert_alpha(),
    ]


def scale_sprite(sprite: pygame.sprite.Sprite, scale: float = 1) -> pygame.sprite.Sprite:
    new_sprite = pygame.sprite.Sprite()
    new_sprite.image = pygame.transform.scale(sprite.image,
                                              (sprite.rect.w * scale, sprite.rect.h * scale)).convert_alpha()
    new_sprite.rect = sprite.image.get_rect()
    return new_sprite


def set_alpha_sprite(sprite: pygame.sprite.Sprite, alpha: int) -> pygame.sprite.Sprite:
    sprite.image.set_alpha(alpha)
    return sprite
