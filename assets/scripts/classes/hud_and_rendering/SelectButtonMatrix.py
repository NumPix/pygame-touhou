import pygame

from assets.scripts.classes.hud_and_rendering.SelectButton import SelectButton
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.math_and_data.enviroment import music_module


class SelectButtonMatrix:
    def __init__(self, position: Vector2, input_matrix: list[list[(str, callable)]], font, defaut_color, selected_color, padding=Vector2(75, 75)):
        self.position = position

        self.matrix = [
            [
                SelectButton(
                    input_matrix[row][column][0],
                    defaut_color,
                    selected_color,
                    font,
                    pygame.Rect(
                        position.x() + padding.x() * column,
                        position.y() + padding.y() * row,
                        padding.x(),
                        padding.y()
                    ),
                    input_matrix[row][column][1]
                )

                for column in range(len(input_matrix[row]))
            ]
            for row in range(len(input_matrix))
        ]

        self.cursor_pos = Vector2.zero()
        self.cursor = Vector2.zero()

    @property
    def cursor(self):
        return self.cursor_pos.to_tuple()

    @cursor.setter
    def cursor(self, value):
        self.matrix[self.cursor_pos.y()][self.cursor_pos.x()].selected = False
        self.cursor_pos = value % Vector2(len(self.matrix[0]), len(self.matrix))
        self.matrix[self.cursor_pos.y()][self.cursor_pos.x()].selected = True

    def move_cursor(self, x: int, y: int):
        self.cursor = Vector2(coords=self.cursor) + Vector2(x, y)

    def draw(self, screen) -> None:
        for row in self.matrix:
            for button in row:
                button.draw(screen)

    def handle_events(self, events: [pygame.event, ...]) -> None:
        for evt in events:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_UP:
                    self.move_cursor(0, -1)
                    music_module.sounds[21](.05)
                if evt.key == pygame.K_DOWN:
                    self.move_cursor(0, 1)
                    music_module.sounds[21](.05)
                if evt.key == pygame.K_LEFT:
                    self.move_cursor(-1, 0)
                    music_module.sounds[21](.05)
                if evt.key == pygame.K_RIGHT:
                    self.move_cursor(1, 0)
                    music_module.sounds[21](.05)
                if evt.key == pygame.K_RETURN or evt.key == pygame.K_z:
                    music_module.sounds[15](.1)
                    self.matrix[self.cursor_pos.y()][self.cursor_pos.x()].trigger()