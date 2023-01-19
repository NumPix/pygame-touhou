import os
from dotenv import load_dotenv

load_dotenv(".env")

PATH = os.getcwd()

WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))
DEFAULT_GLOBAL_VOLUME = float(os.getenv("DEFAULT_GLOBAL_VOLUME"))
DEFAULT_MUSIC_VOLUME = float(os.getenv("DEFAULT_MUSIC_VOLUME"))
SIZE = WIDTH, HEIGHT
GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))
FPS = int(os.getenv("FPS"))
FPS_RATIO = 1

from assets.scripts.classes.sound.MusicModule import MusicModule
from assets.scripts.math_and_data.dbmodule import DAO

db_module = DAO()
music_module = MusicModule()
