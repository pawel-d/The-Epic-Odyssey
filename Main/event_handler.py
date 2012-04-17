#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module is used to handle game's events,
according to the current mode.
"""

__version__ = "0.1"

import pygame
from pygame.locals import *

# Imports modules from local packages
import Interface.actions as actions
import Interface.menus as menus
import Interface.panels as panels
import Interface.windows as windows
import Main.initialization as initialization
import Main.globals as globals_
import Quests.scripting as scripting
import Static.items as items
from Main.constants import *


def normal_mode_events(event):
    """Manages events for the normal mode.

    'event' parameter is a pygame event type.
    """

    # Manages events for when a key is pressed.
    if event.type == KEYDOWN:
        unit = globals_.player_unit

        # Events for the arrow up key
        if event.key == K_UP:
            # Moves player's unit if possible.
            if scripting._possible_to_move(unit, unit.speed, UP):
                # Enters a building if possible.
                if scripting._can_enter(unit):
                    map_ = globals_.current_map

                    number = scripting._can_enter(unit)
                    map_.interior = number

                    unit.rect.x = map_.areas[number - 1][0].x + \
                    int(map_.areas[number - 1][0].width // 2) - \
                    int(unit.rect.width // 2)

                    unit.rect.y = map_.areas[number - 1][0].y - \
                    unit.rect.height

                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone, map_.interior)
                else:
                    unit.move(UP)
            else:
                unit.turn(UP)

        # Events for the arrow down key
        elif event.key == K_DOWN:
            # Moves player's unit if possible.
            if scripting._possible_to_move(unit, unit.speed, DOWN):
                # Enters a building if possible.
                if scripting._can_enter(unit):
                    map_ = globals_.current_map
                    current_interior = map_.interior
                    map_.interior = 0

                    unit.rect.x = map_.areas[current_interior - 1][0].x + \
                    int(map_.areas[current_interior - 1][0].width // 2) - \
                    int(unit.rect.width // 2)

                    unit.rect.y = map_.areas[current_interior - 1][0].y + \
                    unit.rect.height

                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone)
                else:
                    unit.move(DOWN)
            else:
                unit.turn(DOWN)

        # Events for the arrow left key
        elif event.key == K_LEFT:
            # Moves player's unit if possible.
            if scripting._possible_to_move(unit, unit.speed, LEFT):
                unit.move(LEFT)
            else:
                unit.turn(LEFT)

        # Events for the arrow right key
        elif event.key == K_RIGHT:
            # Moves player's unit if possible.
            if scripting._possible_to_move(unit, unit.speed, RIGHT):
                unit.move(RIGHT)
            else:
                unit.turn(RIGHT)

        # Events for the Escape key
        elif event.key == K_ESCAPE:
            pygame.key.set_repeat(0, 0)

            buttons = [menus.Button("ingame_button.bmp", text="Resume",
                                    action="actions.resume_game()"),
                       menus.Button("ingame_button.bmp", text="Load"),
                       menus.Button("ingame_button.bmp", text="Options"),
                       menus.Button("ingame_button.bmp", text="Exit",
                                    action="actions.exit_to_menu()")]

            globals_.current_menu[0] = INGAME_MENU
            globals_.current_menu[1] = menus.InGameMenu("ingame_menu.png",
                                                        buttons)
            globals_.fps = SLOW_FPS
            globals_.current_mode = MENU_MODE

        elif event.key == K_SPACE:
            if not scripting._can_pick_up() is None:
                item = scripting._can_pick_up()

                scripting.remove_item(item)
                globals_.player_unit.inventory.add(item)

        #TEST
        elif event.key == K_e:

            globals_.current_window[0] = FIGHT_WINDOW
            globals_.current_window[1] = windows.ActionDialog()

            globals_.current_opponent.health = MAX_HEALTH

            globals_.current_mode = FIGHTING_MODE
            pygame.key.set_repeat(0, 0)

        #TEST
        elif event.key == K_d:

            globals_.current_panel[0] = DIALOG_PANEL
            globals_.current_panel[1] = panels.DialogPanel(globals_.player_unit)

            globals_.fps = SLOW_FPS
            globals_.current_mode = PANEL_MODE

        # Events for the 'i' key
        elif event.key == K_i:
            globals_.current_window[0] = INVENTORY
            globals_.current_window[1] = windows.Inventory()
            # END OF TEST

            pygame.key.set_repeat(0, 0)
            globals_.fps = SLOW_FPS
            globals_.current_mode = WINDOW_MODE

        map_ = globals_.current_map     # Game's current map
        unit = globals_.player_unit     # Player's current unit

        # Switches to a next zone if possible.
        if unit.rect.x + unit.rect.width + 16 > 1024:
            if map_.zones == 4:
                if map_.zone in (1, 3):
                    map_.zone += 1
                    unit.rect.x = unit.speed + 16
                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone)
        elif unit.rect.x - 16 < 0:
            if map_.zones == 4:
                if map_.zone in (2, 4):
                    map_.zone -= 1
                    unit.rect.x = 1024 - (unit.speed + unit.rect.width + 16)
                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone)
        elif unit.rect.y + unit.rect.height + 16 > 768:
            if map_.zones == 4:
                if map_.zone in (1, 2):
                    map_.zone += 2
                    unit.rect.y = unit.speed + 16
                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone)
        elif unit.rect.y - 16 < 0:
            if map_.zones == 4:
                if map_.zone in (3, 4):
                    map_.zone -= 2
                    unit.rect.y = 768 - (unit.speed + unit.rect.height + 16)
                    globals_.current_bg_sound = ["", True]
                    initialization.update_quest(map_.zone)

    # Manages events for when a key is released.
    elif event.type == KEYUP:
        unit = globals_.player_unit
        unit.stop()


def fight_mode_events(event):
    """Manages events for the fight mode.

    'event' parameter is a pygame event type.
    """

    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            actions.resume_game()
                # Events for the arrow up key
        if event.key == K_UP:
            if globals_.current_window[1].selected in (3, 4):
                globals_.current_window[1].selected -= 2
                if globals_.current_window[1].clicked != 0:
                    globals_.current_window[1].clicked = 0
        # Events for the arrow down key
        elif event.key == K_DOWN:
            if globals_.current_window[1].selected in (1, 2):
                globals_.current_window[1].selected += 2
                if globals_.current_window[1].clicked != 0:
                    globals_.current_window[1].clicked = 0
                # Events for the Return key
        if event.key == K_RIGHT:
            if globals_.current_window[1].selected in (1, 3):
                globals_.current_window[1].selected += 1
                if globals_.current_window[1].clicked != 0:
                    globals_.current_window[1].clicked = 0
        # Events for the arrow down key
        elif event.key == K_LEFT:
            if globals_.current_window[1].selected in (2, 4):
                globals_.current_window[1].selected -= 1
                if globals_.current_window[1].clicked != 0:
                    globals_.current_window[1].clicked = 0
                # Events for the Return key
        elif event.key == K_RETURN:
            buttons = globals_.current_window[1].buttons
            selected = globals_.current_window[1].selected
            globals_.current_window[1].clicked = selected

            exec(buttons[selected - 1].action)


def menu_mode_events(event):
    """Manages events for the menu mode.

    'event' parameter is a pygame event type.
    """

    # Manages events for when a key is pressed.
    if event.type == KEYDOWN:
        # Events for the arrow up key
        if event.key == K_UP:
            if not globals_.current_menu[1].selected == 1:
                globals_.current_menu[1].selected -= 1
                if globals_.current_menu[1].clicked != 0:
                    globals_.current_menu[1].clicked = 0
        # Events for the arrow down key
        elif event.key == K_DOWN:
            if not globals_.current_menu[1].selected == \
            len(globals_.current_menu[1].buttons):
                globals_.current_menu[1].selected += 1
                if globals_.current_menu[1].clicked != 0:
                    globals_.current_menu[1].clicked = 0
        # Events for the Escape key
        elif event.key == K_ESCAPE:
            if globals_.current_menu[0] == INGAME_MENU:
                pygame.key.set_repeat(1, 5)
                globals_.fps = NORMAL_FPS
                globals_.current_mode = NORMAL_MODE
        # Events for the Return key
        elif event.key == K_RETURN:
            buttons = globals_.current_menu[1].buttons
            selected = globals_.current_menu[1].selected
            globals_.current_menu[1].clicked = selected

            exec(buttons[selected - 1].action)


def panel_mode_events(event):

    if event.type == KEYDOWN:

        if event.key == K_RETURN:
            globals_.fps = NORMAL_FPS
            globals_.current_mode = NORMAL_MODE


def window_mode_events(event):
    """Manages events for the inventory mode.

    'event' parameter is a pygame event type.
    """
    if event.type == KEYDOWN:

        if globals_.current_window[0] == INVENTORY and not globals_.current_menu[0] == CONTEXT_MENU or\
        globals_.current_window[0] == FIGHT_INVENTORY and not globals_.current_menu[0] == CONTEXT_MENU:
            if event.key == K_LEFT:
                if not globals_.current_window[1].selected == 1:
                    globals_.current_window[1].selected -= 1
            # Events for the arrow right key
            if event.key == K_RIGHT:
                if not globals_.current_window[1].selected == len(globals_.current_window[1].items):
                    globals_.current_window[1].selected += 1
            if event.key == K_i and globals_.current_window[0] == INVENTORY:
                pygame.key.set_repeat(1, 5)
                globals_.fps = NORMAL_FPS
                globals_.current_mode = NORMAL_MODE
            if event.key == K_ESCAPE and globals_.current_window[0] == FIGHT_INVENTORY:
                globals_.current_window[0] = FIGHT_WINDOW
                globals_.current_window[1] = windows.ActionDialog(globals_.previous_player_action)
                globals_.current_mode = FIGHTING_MODE
            if event.key == K_RETURN  and not len(globals_.player_unit.inventory.items) == 0:
                selected = globals_.current_window[1].selected
                item = globals_.current_window[1].items[selected - 1]
                globals_.current_menu[0] = CONTEXT_MENU
                globals_.current_menu[1] = item.contextMenu
                globals_.current_menu[1].selected = 1
                globals_.current_menu[1].clicked = 0

        elif globals_.current_window[0] == INVENTORY and globals_.current_menu[0] == CONTEXT_MENU or\
        globals_.current_window[0] == FIGHT_INVENTORY and globals_.current_menu[0] == CONTEXT_MENU:
            # Events for the arrow up key
            if event.key == K_UP:
                if not globals_.current_menu[1].selected == 1:
                    globals_.current_menu[1].selected -= 1
                    if globals_.current_menu[1].clicked != 0:
                        globals_.current_menu[1].clicked = 0
            # Events for the arrow down key
            elif event.key == K_DOWN:
                if not globals_.current_menu[1].selected == \
                len(globals_.current_menu[1].buttons):
                    globals_.current_menu[1].selected += 1
                    if globals_.current_menu[1].clicked != 0:
                        globals_.current_menu[1].clicked = 0
            # Events for the Return key
            elif event.key == K_RETURN:
                buttons = globals_.current_menu[1].buttons
                selected = globals_.current_menu[1].selected
                globals_.current_menu[1].clicked = selected

                exec(buttons[selected - 1].action)

if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
