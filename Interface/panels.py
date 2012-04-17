from abc import ABCMeta, abstractmethod, abstractproperty

import pygame

import Main.globals as globals_
from Main.constants import *


class Panel(object):
    """Abstract class used to create in-game panels."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, background, colorkey=GREEN):
        self.background = pygame.image.load(PATH_PANELS + background)
        self.background.set_colorkey(colorkey)


class DialogPanel(Panel):
    """A panel used to display dialogs between characters."""

    def __init__(self, character):
        super(DialogPanel, self).__init__("dialog_panel.bmp")

        self.__dialog = globals_.dialogs.get(character.behavior.dialogs[0])
        self.__index = 0
        self.content = character.name + ": "

    def nextLetter(self):
        if not self.__index + 1 > len(self.__dialog):
            self.content += self.__dialog[self.__index]
            self.__index += 1


class Healthbar(Panel):

    def __init__(self, health, foreground_image="health_foreground.png", background_image="health_background.bmp"):
        super(Healthbar, self).__init__(background_image)

        self.health = health
        self.foreground = pygame.image.load(PATH_PANELS + foreground_image)
        self.foreground.set_colorkey(GREEN)


class Level(Panel):
    def __init__(self, level, background="level.bmp"):
        super(Level, self).__init__(background)

        self.level = level



