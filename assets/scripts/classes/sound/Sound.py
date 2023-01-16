from pygame import mixer
from os.path import join as path_join

class Sound:
    def __init__(self, filename: str, duration: int = 0, fade: int = 0, volume: int = 1,
                 global_volume: float = 1) -> None:

        self.name = filename
        self.sound = mixer.Sound(path_join("assets", "music", filename))
        self.duration = duration
        self.fade = fade
        self.volume = volume
        self.global_volume = global_volume

        self.sound.set_volume(self.volume * self.global_volume)

    def __call__(self, volume) -> None:
        self.sound.set_volume(volume * self.global_volume)
        self.sound.play(0, self.duration, self.fade)

    def change_config(self, duration: int = None, fade_ms: int = None, global_volume: float = None) -> None:
        if duration:
            self.duration = duration
        if fade_ms:
            self.fade = fade_ms
        if global_volume:
            self.global_volume = global_volume
            self.sound.set_volume(self.volume * self.global_volume)

