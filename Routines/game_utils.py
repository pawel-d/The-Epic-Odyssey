#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains functions,
commonly used across the program."""

from __future__ import with_statement

__version__ = "0.1"

import copy
import cPickle
import os
import sys
import traceback

if __name__ == "__main__":
    sys.path[0] = os.getcwd()[:-len("Routines")]

# Imports modules from local packages.
import Interface.windows as windows
import Main.globals as globals_
from Main.constants import *


def load_game_files():
    """Loads and returns game's objects, such as characters,
    items, maps etc.
    """

    try:
        with open(PATH_DATA + "data1.epic", "rb") as data:
            files = cPickle.load(data)
            # validate the files
    except IOError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        return files


def load_game_quest(map_, quest_no, zone=0, interior=0):
    """Loads and returns a single quest."""

    path = map_ + "_" + str(quest_no)

    if not zone == 0:
        # Loads a quest for the specified zone.
        path += "_" + str(zone)
        if not interior == 0:
            # Loads a quest for the specified interior of a building.
            path += "_" + str(interior)

    try:
        # Reads the quest from the file.
        with open(PATH_QUESTS + path + ".src") as data:
            quest = copy.deepcopy(data.read())
    except IOError:
        return "pass"
    else:
        return str(quest)


def load_dialogs(text_file):

    try:
        dialogs = {}
        with open(PATH_TEXTS + text_file, "r") as fh:
            while True:
                tmp = fh.readline()

                if tmp == "":
                    break

                id_ = tmp[2:-1]
                dialog = fh.readline()[2:-1]

                dialogs[id_] = dialog
    except IOError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        return dialogs


def load_game_state():
    """Loads and returns game's previously saved state."""

    try:
        with open(PATH_DATA + "data3.epic", "rb") as data:
            state = cPickle.load(data)
            # validate the files
    except IOError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        return state


def save_game_files(data):
    """Saves game's files, such as characters,
    items and maps to a file.
    """

    try:
        # Saves data to a file.
        with open(PATH_DATA + "data1.epic", "wb") as files:
            cPickle.dump(data, files)
    except IOError as err:
        # Displays an error on the screen.
        windows.show_error(err, traceback.extract_stack()[-1])


def save_game_state(data):
    """Saves game's current state to a file."""

    try:
        # Saves data to a file.
        with open(PATH_DATA + "data2.epic", "wb") as state:
            cPickle.dump(data, state)
    except IOError as err:
        # Displays an error on the screen.
        windows.show_error(err, traceback.extract_stack()[-1])
