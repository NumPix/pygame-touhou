from assets.scripts.classes.SpriteSheet import SpriteSheet

characters = {
    0: {
        "name": "Marisa",
        "speed": 7,
        "sprite-sheet": SpriteSheet("assets/sprites/marisa_forward.png").crop((50, 100)),
        "attack-function": None
    },
    1: {
        "name": "Reimu",
        "speed": 5,
        "sprite-sheet": None,
        "attack-function": None
    },
    2: {
        "name": "Remilia",
        "speed": 6,
        "sprite-sheet": None,
        "attack-function": None
    },
    3: {
        "name": "Koishi",
        "speed": 6,
        "sprite-sheet": None,
        "attack-function": None
    }
}
