#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains procedures used to initialize
different aspects of the program, such as quests or entire games.
"""

__version__ = "0.1"

# Imports modules from local packages.
import Interface.menus as menus
import Main.globals as globals_
import Routines.game_utils as game_utils
from Main.globals import items_placement
from Quests.scripting import *


def init_main_menu():

    globals_.current_mode = MENU_MODE
    globals_.current_menu[0] = MAIN_MENU
    globals_.fps = SLOW_FPS

    # Disables auto key repetition.
    pygame.key.set_repeat(0, 0)

    globals_.current_music = [PATH_MUSIC + "menu.ogg", True]

    buttons = [menus.Button("main_button.bmp", text="New Game",
                            action="actions.new_game()"),
               menus.Button("main_button.bmp", text="Load"),
               menus.Button("main_button.bmp", text="Options"),
               menus.Button("main_button.bmp", text="Quit",
                            action="actions.quit_game()")]

    globals_.current_menu[1] = menus.MainMenu("main_menu.png", buttons,
                                              "game_picture.bmp")


def init_mixer():
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

    # Sets up the game's mixer.
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.Channel(0).set_volume(1.0)


def init_new_game():
    """Initializes a new game."""

    globals_.current_mode = NORMAL_MODE
    globals_.fps = NORMAL_FPS

    loading_screen = pygame.image.load(PATH_WINDOWS + "loading_screen.bmp")

    globals_.display_surface.blit(loading_screen, (0, 0))
    pygame.display.update()

    # Sets key repetition to 1 click every 5 milliseconds.
    pygame.key.set_repeat(1, 5)

    # Loads game' files from 'data1.epic'.
    globals_.game_files = game_utils.load_game_files()
    globals_.dialogs = game_utils.load_dialogs("Test.txt")

    # Loads game's sounds into the memory.
    init_sounds()

    # Initializes the basic quest.
    init_quest("ISLAND", 0)

    # Updates the basic quest to the map's current zone.
    update_quest(globals_.current_map.zone)


def init_sounds():
    globals_.bg_sounds = []
    globals_.bg_sounds.append([pygame.mixer.Sound(PATH_MUSIC + \
                                                  "waterfall.ogg"),
                               PATH_MUSIC + "waterfall.ogg"])
    globals_.bg_sounds.append([pygame.mixer.Sound(PATH_MUSIC + \
                                                  "seagulls.ogg"),
                               PATH_MUSIC + "seagulls.ogg"])


def init_quest(map_, quest_no):
    """Initializes a new quest."""

    # Loads a specified quest.
    quest = game_utils.load_game_quest(map_, quest_no)

    # Assigns the current quest to a global variable.
    globals_.current_quest[0] = quest
    globals_.current_quest[1] = quest_no

    # Executes Python code from the quest.
    try:
        exec(globals_.current_quest[0])
    except Exception as err:
        # Displays an error on the screen.
        windows.show_error(err, traceback.extract_stack()[-1])


def init_saved_game():
    """Initializes a saved game."""

    raise NotImplementedError()


def update_quest(zone, interior=0):
    """Updates the current quest.

    Used when a zone is changed or when player enters a building.
    """

    # Clears all in-game objects.
    globals_.clear_in_game_globals()

    # Loads a quest for the current zone.
    if not zone == 0:
        quest = game_utils.load_game_quest(globals_.current_map.name.capitalize(),
                                           globals_.current_quest[1],
                                           zone=zone, interior=interior)

        # Assigns the current quest to a global variable.
        globals_.current_quest[0] = quest

        # Executes Python code from the quest.
        try:
            exec(globals_.current_quest[0])
        except Exception as err:
            # Displays an error on the screen.
            windows.show_error(err, traceback.extract_stack()[-1])

if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
