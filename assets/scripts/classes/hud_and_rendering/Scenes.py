class Scene:
    def __init__(self):
        self.next = self

    def process_input(self, events):
        pass

    def update(self):
        pass

    def render(self, screen, clock):
        pass

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)


