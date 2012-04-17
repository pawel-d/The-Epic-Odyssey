#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains game's global variables."""

__version__ = "0.1"

import pygame

import NonStatic.characters as characters
import Interface.menus as menus
from Main.constants import *

display_surface = None
tmp = None

game_files = {}                 # Dictionary containing game's files
events = []                     # UNDER CONSTRUCTION!

bg_sounds = []
current_bg_sound = ["", False]  # Game's current background sound
current_mode = NORMAL_MODE      # Game's current mode - 1 for Normal Mode
current_map = None              # Current map to be displayed on the screen
current_menu = [0, None]        # Current menu to be displayed
current_music = ["", False]     # Current music to be played during the game
current_panel = [0, None]
current_quest = ["", 0]         # Game's current quest
current_window = [0, None]      # Game's current window to be displayed.
frame_counter = 0               # Counts the frames of the game
frame_counter_two = 0           # Counts the frames of the game
frame_counter_three = 0
dialogs = {}
fps = NORMAL_FPS

# Fighting mode globals
flee = False                    # If character has fled or not
turn = PLAYER                   # Tells which combatant's turn it is
fight_action_made = False       # Tells if a battle action has been made
damage = 0                      # Holds the damage done by an attack
combat_message = ""                 # Holds the combat log
previous_player_action = 0      # Holds the latest player action

items_placement = []

for i in range(0, 100):
    items_placement.append(True)

player_unit = None              # Player's unit that can be controlled
quit_game = False               # Determines whether to quit the game
units_to_move = []              # A list of units to move

objects_in_game = pygame.sprite.Group()  # A group containing objects in game
units_in_game = pygame.sprite.Group()    # A group containing units in game

#TEST
current_opponent = characters.Human("Yoshi", (PATH_CHARACTERS + "homer.bmp"))
current_opponent.art_image = pygame.image.load(PATH_CHARACTERS + "art_image_opponent.png")


def clear_all():
    """Clears all global variables."""

    global bg_sounds, current_bg_sound, current_mode, current_map, \
    current_music, current_quest, current_menu, current_window, \
    current_quest, events, fps, items_placement, game_files, player_unit, units_to_move, \
    objects_in_game, units_in_game

    bg_sounds = []
    current_bg_sound = ["", False]
    current_mode = NORMAL_MODE
    current_map = None
    current_menu = [0, None]
    current_music = ["", False]
    current_quest = ["", 0]
    current_window = [0, None]
    events = []
    fps = NORMAL_FPS
    game_files = {}
    player_unit = None
    units_to_move = []

    """
    items_placement = []

    for i in range(0, 100):
        items_placement.append(True)
    """

    objects_in_game.empty()
    units_in_game.empty()


def clear_in_game_globals():
    """Clears all the global variables,
    that contain units or objects in game.
    """

    global events, objects_in_game, units_in_game, units_to_move

    objects_in_game.empty()
    units_in_game.empty()

    events = []
    units_to_move = []

if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
