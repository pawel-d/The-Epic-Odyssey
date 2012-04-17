#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for menus to be used in the game."""

__version__ = "0.1"

from abc import ABCMeta, abstractmethod

import pygame
from pygame.locals import *

from Main.constants import *


class Button(pygame.sprite.Sprite):
    """Class used for creating buttons,
    to be used inside of various types of menus.

    Parameters:

    'spritesheet' - a three-items spritesheet for a button 
                   (normal, hovered, clicked)
    'text' - an optional text for the button
    'action' - an optional action to be taken after the button is clicked
    """

    def __init__(self, spritesheet, text="", action=""):

        # Initiates the super class.
        pygame.sprite.Sprite.__init__(self)

        self.__spritesheet = pygame.image.load(PATH_MENUS + spritesheet)
        self.__dimensions = (self.__spritesheet.get_width() // 3,
                             self.__spritesheet.get_height())

        self.__action = action
        self.text = text

        self.image = pygame.Surface((self.__dimensions[0],
                                     self.__dimensions[1]))
        self.image.blit(self.__spritesheet, (0, 0),
                        (0, 0, self.__dimensions[0],
                         self.__dimensions[1]))
        self.image.set_colorkey((0, 0, 255))

        self.rect = self.image.get_rect()

    @property
    def action(self):
        return self.__action

    def click(self):
        """Updates the button's image to the 'clicked' state."""
        self.image.blit(self.__spritesheet, (0, 0),
                        (self.__dimensions[0] * 2, 0,
                         self.__dimensions[0],
                         self.__dimensions[1]))

    def hover(self):
        """Updates the button's image to the 'hovered' state."""
        self.image.blit(self.__spritesheet, (0, 0),
                        (self.__dimensions[0], 0,
                         self.__dimensions[0],
                         self.__dimensions[1]))

    def reset(self):
        """Resets the button's image to the normal state."""
        self.image.blit(self.__spritesheet, (0, 0),
                        (0, 0, self.__dimensions[0],
                         self.__dimensions[1]))


class Menu(object):
    """Abstract class to create various types of menus
    to use in the game.

    Parameters:

    'background' - path to the image for menu's background
    'buttons' - a list of 'Button' objects
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, background, buttons, font_size=48, selected=1):

        if not background == None:
            self.__background = pygame.image.load(PATH_MENUS + background)
        self.__buttons = buttons
        self.fontSize = font_size

        self.__clicked = 0
        self.__selected = selected
        self.__buttons[self.__selected - 1].hover()

    @property
    def background(self):
        return self.__background

    @property
    def buttons(self):
        return self.__buttons

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, click):
        if click > 0:
            self.__clicked = click
            self.__buttons[self.__clicked - 1].click()

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, select):
        if select > 0:
            self.__buttons[self.__selected - 1].reset()

            self.__selected = select
            self.__buttons[self.__selected - 1].hover()


class ContextMenu(Menu):

    def __init__(self, background, buttons, font_size=32):
        super(ContextMenu, self).__init__(background, buttons, font_size)


class InGameMenu(Menu):
    """Creates an in-game menu to be used in the game.

    Parameters:

    'background' - path to the background image of menu
    'buttons' - a list of 'Button' objects
    """

    def __init__(self, background, buttons, font_size=32):
        super(InGameMenu, self).__init__(background, buttons, font_size)


class MainMenu(Menu):

    def __init__(self, background, buttons, picture, font_size=48):
        super(MainMenu, self).__init__(background, buttons, font_size)

        self.picture = pygame.image.load(PATH_MENUS + picture)


if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
