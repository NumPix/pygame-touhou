from pygame import mixer

from os import listdir
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
        self.sound.set_volume(volume)
        self.sound.play(0, self.duration, self.fade)

    def change_config(self, duration: int = None, fade_ms: int = None, global_volume: float = None) -> None:
        if duration:
            self.duration = duration
        if fade_ms:
            self.fade = fade_ms
        if global_volume:
            self.global_volume = global_volume
            self.sound.set_volume(self.volume * self.global_volume)


class MusicModule:

    def __init__(self, volume: float = 1) -> None:

        mixer.init()

        from assets.scripts.math_and_data.enviroment import PATH

        self.sounds = [Sound(path_join(PATH, "assets", "music", "sounds", filename)) for filename in filter(lambda x: x.endswith(".wav"), listdir(path_join(PATH, "assets", "music", "sounds")))]
        self.sounds.sort(key=lambda sound: sound.name)
        self.bg_volume = volume

    def change_sound_config(self, index: int, duration: int = None, fade: int = None, global_volume: float = None) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)

        if index in range(len(self.sounds)):
            self.sounds[index].change_config(duration, fade, global_volume)

    def set_global_volume(self, global_volume: float) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)
        for sound in self.sounds:
            sound.change_config(global_volume=global_volume)

    def __getitem__(self, index: int) -> Sound | None:
        if index in range(len(self.sounds)):
            return self.sounds[index]
        return None

    @staticmethod
    def play_music(background: str, volume: float = .3) -> None:
        from assets.scripts.math_and_data.enviroment import PATH
        mixer.music.load(path_join(PATH, "assets", "music", background))
        mixer.music.set_volume(volume)
        mixer.music.play(-1)

    @staticmethod
    def stop_music() -> None:
        mixer.music.unload()
