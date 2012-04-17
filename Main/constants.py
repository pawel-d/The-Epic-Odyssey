#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains game's global constants."""

__version__ = "0.1"

import sys


# Paths to various directories for file access
if sys.platform == "win32":
    PATH_DATA = sys.path[0] + "\\Data\\"
    PATH_FONTS = PATH_DATA + "\\Fonts\\"

    PATH_GRAPHICS = PATH_DATA + "\\Graphics\\"
    PATH_CHARACTERS = PATH_GRAPHICS + "\\Characters\\"
    PATH_ITEMS = PATH_GRAPHICS + "\\Items\\"
    PATH_MAPS = PATH_GRAPHICS + "\\Maps\\"
    PATH_MENUS = PATH_GRAPHICS + "\\Menus\\"
    PATH_PANELS = PATH_GRAPHICS + "\\Panels\\"
    PATH_WINDOWS = PATH_GRAPHICS + "\\Windows\\"

    PATH_MISC = PATH_DATA + "\\Misc\\"
    PATH_QUESTS = PATH_DATA + "\\Quests\\"

    PATH_SOUNDS = PATH_DATA + "\\Sounds\\"
    PATH_MUSIC = PATH_SOUNDS + "\\Music\\"

    PATH_TEXTS = PATH_DATA + "\\Texts\\"
else:
    PATH_DATA = sys.path[0] + "/Data/"
    PATH_FONTS = PATH_DATA + "/Fonts/"

    PATH_GRAPHICS = PATH_DATA + "/Graphics/"
    PATH_CHARACTERS = PATH_GRAPHICS + "/Characters/"
    PATH_ITEMS = PATH_GRAPHICS + "/Items/"
    PATH_MAPS = PATH_GRAPHICS + "/Maps/"
    PATH_MENUS = PATH_GRAPHICS + "/Menus/"
    PATH_PANELS = PATH_GRAPHICS + "/Panels/"
    PATH_WINDOWS = PATH_GRAPHICS + "/Windows/"

    PATH_MISC = PATH_DATA + "/Misc/"
    PATH_QUESTS = PATH_DATA + "/Quests/"

    PATH_SOUNDS = PATH_DATA + "/Sounds/"
    PATH_MUSIC = PATH_SOUNDS + "/Music/"

    PATH_TEXTS = PATH_DATA + "/Texts/"

# Amount of frames per second
NORMAL_FPS = 25
SLOW_FPS = 5

# Window size parameters
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Directions
UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6
IDLE = 0

# Fight constants
PLAYER = 1
OPPONENT = 2
MELEE_ATTACK = 1
RANGED_ATTACK = 2
USE_ITEM = 3
FLEE = 4

# Game modes
NORMAL_MODE = 1
FIGHTING_MODE = 2
MENU_MODE = 3
PANEL_MODE = 4
WINDOW_MODE = 5

# Window constants
INVENTORY = 1
FIGHT_WINDOW = 2
FIGHT_INVENTORY = 3

# Menu constants
MAIN_MENU = 1
INGAME_MENU = 2
CONTEXT_MENU = 3

# Panel constants
DIALOG_PANEL = 1

# Items
MEDICINE = 1
JEWEL = 2

ITEMS = [MEDICINE, JEWEL]

# Character constants
MAX_HEALTH = 100

# Attitudes
FRIEND = 1
ENEMY = 2

if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
