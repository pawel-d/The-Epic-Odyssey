#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This modules contains actions to use for button listeners."""
import random
import pygame

import Main.globals as globals_
import Interface.windows as windows
import Interface.menus as menus
import Main.initialization as initialization
from Main.constants import *


def cancel_menu():
    globals_.current_menu = [0, None]


def disable_action_dialog_buttons():
    buttons = [menus.Button("action_dialog_button_all_locked.bmp", text="Melee Attack"),
               menus.Button("action_dialog_button_all_locked.bmp", text="Ranged Attack"),
               menus.Button("action_dialog_button_all_locked.bmp", text="Use Item"),
               menus.Button("action_dialog_button_all_locked.bmp", text="Flee")]
    globals_.current_window[1] = windows.ActionDialog(1, buttons)


def enable_action_dialog_buttons(selected):
    globals_.current_window[1] = windows.ActionDialog(selected)


def exit_to_menu():
    globals_.clear_all()
    globals_.current_bg_sound[1] = True
    globals_.current_music[1] = True

    initialization.init_main_menu()


def melee_attack(unit1, unit2):
    if unit1 == globals_.player_unit:
        globals_.fight_action_made = True
        globals_.previous_player_action = MELEE_ATTACK

    hit_chance = random.randint(1, 10)

    if hit_chance == 1:
        globals_.combat_message = "Melee Attack Missed!"
    else:
        damage = random.randint(10, 15)
        globals_.damage = damage
        globals_.combat_message = "Melee Attack hits for " + str(damage) + " Damage!"


def new_game():
    globals_.clear_all()
    initialization.init_new_game()


def opponent_action():
    action = random.randint(1, 2)

    if action == 1 or globals_.current_opponent.weapon == None:
        melee_attack(globals_.current_opponent, globals_.player_unit)
    elif action == 2:
        ranged_attack(globals_.current_opponent, globals_.player_unit)


def quit_game():
    globals_.quit_game = True


def reset_fighting():
    globals_.frame_counter = 0
    globals_.frame_counter_two = 0
    globals_.frame_counter_three = 0
    globals_.turn = PLAYER


def resume_game():
    globals_.fps = NORMAL_FPS
    globals_.current_mode = NORMAL_MODE
    globals_.current_menu = [0, None]

    pygame.key.set_repeat(1, 5)


def ranged_attack(unit1, unit2):

    if not unit1.weapon == None and not unit1.weapon == "":
        if unit1 == globals_.player_unit:
            globals_.fight_action_made = True
            globals_.previous_player_action = RANGED_ATTACK

        hit_chance = random.randint(1, 6)
        if hit_chance <= 1:
            globals_.combat_message = "Ranged Attack Missed!"

        else:
            damage = random.randint(25, 35)
            globals_.damage = damage
            globals_.combat_message = "Ranged Attack hits for " + str(damage) + " Damage!"


def flee(unit1, unit2):

    max_rand_value = 10
    flee_chance = random.randint(1, max_rand_value)
    globals_.fight_action_made = True
    globals_.previous_player_action = FLEE

    if flee_chance > 2:
        globals_.flee = True
        resume_game()

    else:
        globals_.combat_message = "Flee Attempt Failed!"


def fighting_mode_inventory():
    globals_.previous_player_action = USE_ITEM
    globals_.current_window[0] = FIGHT_INVENTORY
    globals_.current_window[1] = windows.Inventory()
    globals_.current_mode = WINDOW_MODE


def use_item(item):
    globals_.player_unit.use(item)
