# words.py — Word lists for all 3 levels

WORDS = {
    "beginner": [
        "CAT",
        "DOG",
        "SUN",
        "HAT",
        "BUS",
        "APPLE",
        "BALL",
        "FISH",
        "BIRD",
        "FROG"
    ],

    "intermediate": [
        "MANGO",
        "GRAPE",
        "TIGER",
        "LEMON",
        "CAMEL",
        "PLANT",
        "STORM",
        "BRAVE",
        "CLOCK",
        "FLAME"
    ],

    "advanced": [
        "ELEPHANT",
        "DOLPHIN",
        "VOLCANO",
        "PYRAMID",
        "BLANKET",
        "CLUSTER",
        "DIAMOND",
        "FEATHER",
        "JOURNEY",
        "LANTERN"
    ]
}


def get_word(level):
    """Returns a random word for the given level"""
    import random
    return random.choice(WORDS[level])