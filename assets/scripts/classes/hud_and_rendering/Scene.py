class Scene:
    def __init__(self):
        self.next = self

    def process_input(self, events) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, screen, clock) -> None:
        pass

    def switch_to_scene(self, next_scene) -> None:
        self.next = next_scene
