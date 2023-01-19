from pygame import mixer

from os import listdir
from os.path import join as path_join

from assets.scripts.classes.sound.Sound import Sound
from assets.scripts.math_and_data.enviroment import DEFAULT_GLOBAL_VOLUME, DEFAULT_MUSIC_VOLUME


class MusicModule:

    def __init__(self, volume: float = 1) -> None:

        mixer.init()

        from assets.scripts.math_and_data.enviroment import PATH

        self.sounds = [
            Sound(
                path_join(PATH, "assets", "music", "sounds", filename),
                global_volume=DEFAULT_GLOBAL_VOLUME
            )

            for filename in filter(
                lambda x: x.endswith(".wav"),
                listdir(path_join(PATH, "assets", "music", "sounds"))
            )
        ]

        self.sounds.sort(key=lambda sound: sound.name)
        self.bg_volume = volume

    def change_sound_config(self, index: int, duration: int = None, fade: int = None,
                            global_volume: float = None) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)

        if index in range(len(self.sounds)):
            self.sounds[index].change_config(duration, fade, global_volume)

    def set_global_volume(self, global_volume: float) -> None:
        mixer.music.set_volume(self.bg_volume * global_volume)
        for sound in self.sounds:
            sound.change_config(global_volume=global_volume)

    def __getitem__(self, index: int) -> Sound:
        if index in range(len(self.sounds)):
            return self.sounds[index]
        return None

    @staticmethod
    def play_music(background: str, volume: float = DEFAULT_MUSIC_VOLUME) -> None:
        from assets.scripts.math_and_data.enviroment import PATH
        mixer.music.load(path_join(PATH, "assets", "music", background))
        mixer.music.set_volume(volume)
        mixer.music.play(-1)

    @staticmethod
    def stop_music() -> None:
        mixer.music.unload()
