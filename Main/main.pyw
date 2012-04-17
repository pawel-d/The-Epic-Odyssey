#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This is the game's main and most important module.
It contains the main procedure, which is responsible for the game loop
and events handling.
"""

__version__ = "0.1"

import os
import sys

import pygame
from pygame.locals import *

# Fixes the program's main directory to use in local packages and modules.
if __name__ == "__main__":
    sys.path[0] = os.getcwd()[:-len("Main")]

# Imports modules from local packages.
import Interface.actions as actions
import Interface.panels as panels
import Main.event_handler as event_handler
import Main.globals as globals_
import Main.initialization as initialization
import Routines.cpu_requests as cpu_requests
from Main.constants import *


def main():
    """Program's core and main procedure, manages game's engine.

    Parameters:

    'new_game' - used to determine whether to start a new game
                 or to load the previous state.
    """

    # Starts the game's engine.
    pygame.init()

    # Initializes game's audio.
    initialization.init_mixer()

    # Initializes main menu.
    initialization.init_main_menu()

    # Additional game constants
    global FPS_CLOCK, DISPLAY_SURFACE
    FPS_CLOCK = pygame.time.Clock()             # Game's internal clock

    DISPLAY_SURFACE = \
    pygame.display.set_mode((WINDOW_WIDTH,
                             WINDOW_HEIGHT))    # Game's main display

    globals_.display_surface = DISPLAY_SURFACE

    # Sets the window's title to 'The Epic Odyssey'.
    pygame.display.set_caption("The Epic Odyssey")

    # Hides mouse cursor.
    pygame.mouse.set_visible(False)

    # TEST
    font2 = pygame.font.Font(None, 18)

    # --- GAME LOOP --- #
    run_game = True
    while run_game:
        if globals_.quit_game:
            break
        # Manages game's events.
        for event in pygame.event.get():
            if event.type == QUIT:
                # Quits the game.
                run_game = False
            # Sends events to be managed by the event handler.
            if globals_.current_mode == NORMAL_MODE:
                event_handler.normal_mode_events(event)
            elif globals_.current_mode == FIGHTING_MODE:
                event_handler.fight_mode_events(event)
            elif globals_.current_mode == MENU_MODE:
                event_handler.menu_mode_events(event)
            elif globals_.current_mode == PANEL_MODE:
                event_handler.panel_mode_events(event)
            elif globals_.current_mode == WINDOW_MODE:
                event_handler.window_mode_events(event)

        # Runs the game loop for the normal mode.
        if globals_.current_mode == NORMAL_MODE:
            # Manages CPU units (i.e. movement, speaking etc).
            cpu_requests.manage_units()

            # Manages quest events.
            cpu_requests.manage_events()

            # Displays the current map on the screen.
            DISPLAY_SURFACE.blit(globals_.current_map.textures, (0, 0))

            # Displays objects and CPU units on the current map.
            if len(globals_.objects_in_game) > 0:
                for obj in globals_.objects_in_game.sprites():
                    DISPLAY_SURFACE.blit(obj.image, obj.rect)
            if len(globals_.units_in_game) > 0:
                for un in globals_.units_in_game.sprites():
                    DISPLAY_SURFACE.blit(un.image, un.rect)

            # Displays player's unit on the current map.
            if not globals_.player_unit is None:
                DISPLAY_SURFACE.blit(globals_.player_unit.image,
                                     globals_.player_unit.rect)

        elif globals_.current_mode == FIGHTING_MODE:
            # Font for action dialog
            font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf",
                                    globals_.current_window[1].fontSize)
            font.set_italic(True)
            # background for FIGHTING_MODE
            map_landscape = globals_.current_map.landscape

            # combatants images
            opponent_image = globals_.current_opponent.art_image
            player_image = globals_.player_unit.art_image
            # action dialog buttons
            buttons = globals_.current_window[1].buttons
            # action_dialog window
            action_dialog = globals_.current_window[1].action_dialog_window
            # dimensions of action dialog
            dimensions_action_dialog = (globals_.current_window[1].action_dialog_window.get_width(),\
                                        globals_.current_window[1].action_dialog_window.get_height())
            # button dimensions
            button_dimensions = (dimensions_action_dialog[0] // 2,\
                                              dimensions_action_dialog[1] // 2)
            # coordinates for the action dialog
            x = globals_.WINDOW_WIDTH - (dimensions_action_dialog[0] + 24)
            y = globals_.WINDOW_HEIGHT - (dimensions_action_dialog[1] + 24)

            # blits background, character images and action dialog
            DISPLAY_SURFACE.blit(map_landscape, (0, 0))
            DISPLAY_SURFACE.blit(opponent_image,\
                                (globals_.WINDOW_WIDTH - (opponent_image.get_width() + 24), 130))
            DISPLAY_SURFACE.blit(player_image,\
                                (24, globals_.WINDOW_HEIGHT - (player_image.get_height() + 48)))
            DISPLAY_SURFACE.blit(action_dialog, (x, y))

            # assign button coordinates and player coordinates
            player_coords = [x, y]  # used for blitting player level and health panel
            button_coords = [x, y]  # used for blitting buttons

            button_count = 0    # holds the number of the current button to be blitted
            for button in buttons:
                # blit button depending on number
                if button_count == 0:
                    x = button_coords[0]
                    y = button_coords[1]
                elif button_count == 1:
                    x = button_coords[0] + button_dimensions[0]
                    y = button_coords[1]
                elif button_count == 2:
                    x = button_coords[0]
                    y = button_coords[1] + button_dimensions[1]
                elif button_count == 3:
                    x = button_coords[0] + button_dimensions[0]
                    y = button_coords[1] + button_dimensions[1]

                # Displays the button on the screen.
                DISPLAY_SURFACE.blit(button.image, (x, y))

                rendered = font.render(button.text, True, BLACK)

                # Displays text on the button.
                DISPLAY_SURFACE.blit(rendered,
                                    (x + (button_dimensions[0] - \
                                    rendered.get_width()) // 2,
                                    y + (button_dimensions[1] - \
                                    rendered.get_height()) // 2))
                # next button
                button_count += 1
            # creates the players health and level panel
            player_healthbar = panels.Healthbar(globals_.player_unit.health)
            player_level = panels.Level(globals_.player_unit.level)
            # creates the opponents health and level panel
            opponent_healthbar = panels.Healthbar(globals_.current_opponent.health)
            opponent_level = panels.Level(globals_.current_opponent.level)
            # a list for the player and opponent containing the character data, healthbar and level
            player = [globals_.player_unit, player_healthbar, player_level]
            opponent = [globals_.current_opponent, opponent_healthbar, opponent_level]
            # a list of the lists above 
            units_in_battle = [player, opponent]
            # coordinates for blitting player and opponent health and level panel
            player_coords[1] -= 12 + 32
            opponent_coords = [24, 24]

            # coords for blitting the level panel
            coords = player_coords
            # loop for blitting the level panel
            for unit in units_in_battle:
                # if unit is opponent use opponent coordinates
                if unit[0] == globals_.current_opponent:
                    coords = opponent_coords
                # blit the level panel background
                DISPLAY_SURFACE.blit(unit[2].background,\
                                     (coords[0], coords[1]))
                # create the text to blit the current level of unit
                rendered = font.render(str(unit[0].level), True, BLACK)
                font.set_italic(False)
                # blit the level text on the background
                DISPLAY_SURFACE.blit(rendered, ((coords[0] + \
                                    (unit[2].background.get_width()\
                                    - rendered.get_width()) // 2),\
                                    (coords[1] + 3 + \
                                    (unit[2].background.get_height()\
                                    - rendered.get_height()) // 2)))

            # increase coordinates for player and opponent to blit the healthbar
            player_coords[0] += 12 + 32
            opponent_coords[0] += 12 + 32
            # font for blitting health percentage
            font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf", 20)
            font.set_italic(True)
            # loop for blitting health panel
            for unit in units_in_battle:
                # if unit is player set player coords and health
                if unit[0] == globals_.player_unit:
                    coords = player_coords
                    current_health = globals_.player_unit.health
                # if unit is opponent set opponent coords and health
                elif unit[0] == globals_.current_opponent:
                    coords = opponent_coords
                    current_health = globals_.current_opponent.health
                # if it is the opponent's turn to act and players health is being blitted
                if globals_.turn == OPPONENT and unit[0] == globals_.player_unit:
                    # initialize frame counter for timing opponents turn
                    globals_.frame_counter += 1
                    # if frame counter is 25 then opponent makes his move
                    if globals_.frame_counter == 25 and globals_.current_opponent.health > 0:
                        actions.opponent_action()
                        combat_message = globals_.current_opponent.name + "'s "\
                        + globals_.combat_message   # set combat log text
                    # if frame counter is 50 then switch action made to True
                    if globals_.frame_counter == 50:
                        globals_.fight_action_made = True
                    # if action made is true
                    if globals_.fight_action_made == True:
                        globals_.turn = PLAYER                 # switch to player's turn
                        globals_.fight_action_made = False     # action made set to false
                        if globals_.player_unit.health > 0:
                            actions.enable_action_dialog_buttons(globals_.previous_player_action)  # enable action dialog buttons
                        globals_.frame_counter = 0              # reset frame counter
                    # subtract the damage done by opponent from player health
                    current_health = unit[0].health
                    unit[0].health -= globals_.damage
                    globals_.damage = 0
                # if it is the player's turn to act and opponents health is being blitted
                if globals_.turn == PLAYER and unit[0] == globals_.current_opponent:
                    # if action made is true
                    if globals_.fight_action_made == True:
                        combat_message = globals_.player_unit.name + "'s "\
                        + globals_.combat_message    # set combat log text
                        # if flee is false
                        if globals_.flee == False:
                            globals_.turn = OPPONENT                    # switch to opponent's turn
                            actions.disable_action_dialog_buttons()     # disable dialog buttons
                        # if flee is true
                        elif globals_.flee == True:
                            globals_.flee = False                       # set flee to false
                        globals_.fight_action_made = False             # put action made back to false
                    # subtract the damage done by player from opponent health
                    current_health = unit[0].health
                    unit[0].health -= globals_.damage
                    globals_.damage = 0
                # if the current health is below 0 set it to 0
                if current_health < 0:
                    current_health = 0
                # calculate the current health scale from max health
                current_healthbar_scale = ((float(current_health) /\
                                            float(MAX_HEALTH)) *\
                                            float(unit[1].background.get_width()\
                                                  - 8))
                # create the rect object to display the current health
                health_rect = pygame.Rect(coords[0] + 4, coords[1] + 4,\
                                          current_healthbar_scale, 22)
                # blit the health panel background
                DISPLAY_SURFACE.blit(unit[1].background,\
                                    (coords[0], coords[1]))
                # blit the current health
                pygame.draw.rect(DISPLAY_SURFACE, RED, health_rect, 0)
                # blit the the health panel foreground
                DISPLAY_SURFACE.blit(unit[1].foreground,\
                                    (coords[0], coords[1]))
                # calculate the health percentage
                health_percentage = (current_healthbar_scale\
                                     / float(unit[1].background.get_width() - 8))\
                                     * 100
                # render font for blitting health percentage
                rendered = font.render(str(health_percentage) + "%", True,\
                                      BLACK)
                # blit health percentage on health bar
                DISPLAY_SURFACE.blit(rendered, ((coords[0] +\
                                    (unit[1].background.get_width()\
                                    - rendered.get_width()) // 2),\
                                    (coords[1] + 3 + \
                                    (unit[1].background.get_height()\
                                    - rendered.get_height()) // 2)))
            # check if fight text is not ""
            if not globals_.combat_message == "":
                font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf", 40)
                font.set_italic(True)
                globals_.frame_counter_two += 1     # start frame counter No 2
                if globals_.frame_counter in (0, 24):
                    color = BLUE
                elif globals_.frame_counter in (25, 50):
                    color = RED
                rendered = font.render(combat_message, True, color)
                combat_message_background = pygame.image.load(PATH_WINDOWS + "combat_message_background.png")
                DISPLAY_SURFACE.blit(combat_message_background, ((WINDOW_WIDTH -\
                                                 combat_message_background.get_width()) // 2,\
                                                (WINDOW_HEIGHT -\
                                                  combat_message_background.get_height()) // 2))
                # blit combat log on screen
                DISPLAY_SURFACE.blit(rendered, ((WINDOW_WIDTH -\
                                                 rendered.get_width()) // 2,\
                                                (WINDOW_HEIGHT -\
                                                  rendered.get_height()) // 2))
            # when 2 seconds have passed set fight text to "" and reset counter
            if globals_.frame_counter_two == 50:
                globals_.combat_message = ""
                globals_.frame_counter_two = 0

            # if the health of the opponent or player goes below 1
            if globals_.player_unit.health < 1 or globals_.current_opponent.health < 1:
                actions.disable_action_dialog_buttons   # disable action dialog buttons
                globals_.frame_counter_three += 1             # frame counter initialized
                # if player health is below 1
                if globals_.player_unit.health < 1:
                    # if frame counter is 60
                    if globals_.frame_counter_three == 50:
                        actions.exit_to_menu()      # exit to menu
                        actions.reset_fighting()    # set next turn to be player's
                    outcome = pygame.image.load(PATH_WINDOWS + "you_lost.png")  # set outcome picture to lost
                # if opponent health is below 1
                elif globals_.current_opponent.health < 1:
                    # if frame counter is 60
                    if globals_.frame_counter_three == 50:
                        actions.resume_game()       # resume game
                        actions.reset_fighting()    # set next turn to be player's
                    outcome = pygame.image.load(PATH_WINDOWS + "you_won.png")   # set outcome picture to won
                # display outcome picture
                DISPLAY_SURFACE.blit(outcome,\
                                     ((WINDOW_WIDTH - outcome.get_width()) // 2,\
                                     ((WINDOW_HEIGHT - outcome.get_height()) // 3)))

        # Runs the game loop for the menu mode.
        elif globals_.current_mode == MENU_MODE:

            # In-game font
            font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf",
                                    globals_.current_menu[1].fontSize)
            font.set_italic(True)

            if globals_.current_menu[0] == MAIN_MENU:
                DISPLAY_SURFACE.blit(globals_.current_menu[1].picture, (0, 0))
                offset = 24
            elif globals_.current_menu[0] == INGAME_MENU:
                # Displays the filtered version of the current map on the screen.
                DISPLAY_SURFACE.blit(globals_.current_map.filtered, (0, 0))
                offset = 0

            if globals_.current_menu[0] in [MAIN_MENU, INGAME_MENU]:
                background = globals_.current_menu[1].background
                coords = ((WINDOW_WIDTH - background.get_width()) // 2,
                          (WINDOW_HEIGHT - background.get_height()) // 2)

                # Displays the current menu's background on the screen.
                DISPLAY_SURFACE.blit(background,
                                     (coords[0], coords[1]),
                                     (0, 0, background.get_width(),
                                      background.get_height()))
                buttons = globals_.current_menu[1].buttons

                # Adds and displays menu buttons on the screen.
                for button in buttons:
                    x = coords[0] + (background.get_width() - \
                                     button.rect.width) // 2
                    y = coords[1] + (background.get_height() - \
                                     (((button.rect.height + 24) * \
                                       len(buttons)) \
                                      - 24)) // 2

                    # Displays the button on the screen.
                    DISPLAY_SURFACE.blit(button.image,
                                         (x, y + offset))

                    rendered = font.render(button.text, True, (0, 0, 0))

                    # Displays text on the button.
                    DISPLAY_SURFACE.blit(rendered,
                                         (x + (button.rect.width - \
                                               rendered.get_width()) // 2,
                                          y + offset + (button.rect.height - \
                                                        rendered.get_height()) // 2))
                    offset += button.rect.height + 24

        # Runs the game loop for the panel mode.
        elif globals_.current_mode == PANEL_MODE:

            if globals_.current_panel[0] == DIALOG_PANEL:
                panel = globals_.current_panel[1]

                DISPLAY_SURFACE.blit(panel.background,
                                     ((WINDOW_WIDTH - panel.background.get_width()) // 2,
                                      WINDOW_HEIGHT - panel.background.get_height() - 10),
                                     (0, 0,
                                      panel.background.get_width(),
                                      panel.background.get_height()))

                font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf",
                                        14)
                font.set_italic(True)
                text = font.render(panel.content, True, (0, 0, 255))

                DISPLAY_SURFACE.blit(text,
                                     ((WINDOW_WIDTH - panel.background.get_width()) // 2,
                                      WINDOW_HEIGHT - panel.background.get_height() - 10),
                                     (0, 0,
                                      panel.background.get_width(),
                                      panel.background.get_height()))

                panel.nextLetter()

        # Runs the game loop for the window mode.
        elif globals_.current_mode == WINDOW_MODE:

            if globals_.current_window[0] == INVENTORY or\
            globals_.current_window[0] == FIGHT_INVENTORY:
                inventory = globals_.current_window[1]
                DISPLAY_SURFACE.blit(inventory.background, (0, 0),
                                     (0, 0,
                                      inventory.dimensions[0],
                                      inventory.dimensions[1]))

                x, y = 0, 0
                for item in inventory.items:
                    DISPLAY_SURFACE.blit(item.icon,
                                         (x + 12, y + 12))
                    if x + 12 <= inventory.dimensions[0] - 128:
                        x += 128
                    else:
                        x = 0
                        if y + 12 <= inventory.dimensions[1] - 128:
                            y += 128

                if globals_.current_menu[0] == CONTEXT_MENU:

                    font = pygame.font.Font(PATH_FONTS + "LithosPro-Black.otf",
                                            globals_.current_menu[1].fontSize)
                    font.set_italic(True)

                    offset = 0
                    background = globals_.current_menu[1].background
                    coords = ((WINDOW_WIDTH - background.get_width()) // 2,
                              (WINDOW_HEIGHT - background.get_height()) // 2)

                    # Displays the current menu's background on the screen.
                    DISPLAY_SURFACE.blit(background,
                                         (coords[0], coords[1]),
                                         (0, 0, background.get_width(),
                                          background.get_height()))
                    buttons = globals_.current_menu[1].buttons

                    # Adds and displays menu buttons on the screen.
                    for button in buttons:
                        x = coords[0] + (background.get_width() - \
                                         button.rect.width) // 2
                        y = coords[1] + (background.get_height() - \
                                        (((button.rect.height + 24) * \
                                        len(buttons)) \
                                        - 24)) // 2

                        # Displays the button on the screen.
                        DISPLAY_SURFACE.blit(button.image, (x, y + offset))

                        rendered = font.render(button.text, True, (0, 0, 0))

                                        # Displays text on the button.
                        DISPLAY_SURFACE.blit(rendered,
                                            (x + (button.rect.width - \
                                            rendered.get_width()) // 2,
                                            y + offset + (button.rect.height - \
                                            rendered.get_height()) // 2))
                        offset += button.rect.height + 24

        # Sets the music to be played during the game.
        if globals_.current_music[1] is True \
        or not pygame.mixer.music.get_busy():

                # Stops the current music.
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                # Prevents the new music from being stopped.
                globals_.current_music[1] = False

                # Loads the new music to memory and plays it.
                if not globals_.current_music[0] == "":
                    pygame.mixer.music.load(globals_.current_music[0])
                    pygame.mixer.music.play(0)

        # Sets the music to be played during the game.
        if globals_.current_bg_sound[1] is True:

            # Stops the current music.
            if pygame.mixer.Channel(0).get_busy():
                pygame.mixer.Channel(0).stop()

            # Prevents the new music from being stopped.
            globals_.current_bg_sound[1] = False

            # Loads the new music to memory and plays it.
            if not globals_.current_bg_sound[0] == "":
                for i, x in enumerate(globals_.bg_sounds):
                    if globals_.bg_sounds[i][1] == \
                    globals_.current_bg_sound[0]:
                        pygame.mixer.Channel(0).play(globals_.bg_sounds[i][0],
                                                     loops=-1)

        # TEST
        amount_of_fps = font2.render("FPS: " + str(int(FPS_CLOCK.get_fps())), True, (255, 0, 0))
        DISPLAY_SURFACE.blit(amount_of_fps, (20, 20))
        # END OF TEST

        # Updates the game's main display.
        pygame.display.update()

        # Sets amount of frames per second to 30.
        FPS_CLOCK.tick(globals_.fps)

    # Quits the game after the loop is over.
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

# Initializes the main procedure only if the module is run directly.
if __name__ == "__main__":
    main()
