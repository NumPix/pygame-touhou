import os
from dotenv import load_dotenv

from assets.scripts.math_and_data.dbmodule import DAO

load_dotenv(".env")


WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))
SIZE = WIDTH, HEIGHT
GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))
FPS = int(os.getenv("FPS"))
FPS_RATIO = 1

db_module = DAO()
