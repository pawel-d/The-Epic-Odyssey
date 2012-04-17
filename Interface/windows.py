#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains windows
to be used for various purposes within the game.
"""

__version__ = "0.1"

import os
from abc import ABCMeta, abstractmethod

import pygame
from pygame.locals import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Interface.menus as menus
import Main.globals as globals_
from Main.constants import *

# Local constants
BORDER_WIDTH = 32

# Path constants
PATH = sys.path[0] + "Data//Graphics//Windows//"
PATH2 = sys.path[0] + "Data//Fonts//"


def show_error(err, trace):
    """Displays an error on the screen.

    Parameters:

    err - error object
    trace - traceback object
    """

    # Creates an instance of a new QApplication.
    app = QApplication(sys.argv)

    # Specifies the error message.
    err_message = str(type(err).__name__ + ": " + str(err).capitalize() + "." +
                      "\nmodule: " + os.path.basename(trace[0]) +
                      "; line: " + str(trace[1]))

    # Displays a message box with the specified error message.
    QMessageBox.critical(None, "Error", err_message)

    # Exits the program after the message box is closed.
    sys.exit(app.exec_())


class Windows(object):
    """Abstract class used to create in-game windows."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, background, dimensions):
        self.background = pygame.image.load(PATH_WINDOWS + background)
        self.dimensions = dimensions


class ActionDialog(menus.Menu):

    def __init__(self, selected=1, buttons=[menus.Button("action_dialog_button.bmp", text="Melee Attack",
                                                        action="actions.melee_attack(globals_.player_unit, globals_.current_opponent)"),
                                            menus.Button("action_dialog_button.bmp", text="Ranged Attack",
                                                        action="actions.ranged_attack(globals_.player_unit, globals_.current_opponent)"),
                                            menus.Button("action_dialog_button.bmp", text="Use Item",
                                                        action="actions.fighting_mode_inventory()"),
                                            menus.Button("action_dialog_button.bmp", text="Flee",
                                                        action="actions.flee(globals_.player_unit, globals_.current_opponent)")]):
        super(ActionDialog, self).__init__(None, buttons=buttons, font_size=26, selected=selected)

        self.action_dialog_window = pygame.image.load(PATH_WINDOWS + "action_dialog.bmp")
        self.__buttons = buttons

        self.selected = selected
        self.action_dialog_window.set_colorkey(GREEN)
        self.__buttons[3].reset()
        if globals_.player_unit.weapon == None or globals_.player_unit.weapon == "":
            self.__buttons[1] = menus.Button("action_dialog_button_locked.bmp", text="Ranged Attack")

    @property
    def buttons(self):
        return self.__buttons

    @buttons.setter
    def buttons(self, new_buttons):
        self.__buttons = new_buttons


class CharacterWindow(Windows):
    """Character's window to be displayed in the game."""

    def __init__(self):
        raise NotImplementedError


class Inventory(Windows):

    def __init__(self):
        super(Inventory, self) .__init__("inventory_window.bmp",
                                         (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.items = []

        for i in globals_.player_unit.inventory.items:
            self.items.append(i)

        self.__selected = 1

        if len(self.items) > 0:
            self.items[self.__selected - 1].select()

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, select):
        self.items[self.__selected - 1].reset()

        self.__selected = select
        self.items[self.__selected - 1].select()


if __name__ == "__main__":
    class DirectRunError(Exception): pass
    
    raise DirectRunError("This module cannot be run directly.")
