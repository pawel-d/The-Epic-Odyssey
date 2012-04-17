#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for various items
to be used in the game.
"""

__version__ = "0.1"

from abc import ABCMeta, abstractmethod

import pygame

import Interface.menus as menus
from Main.constants import *


class Item(pygame.sprite.Sprite):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, description, image, icon, context_menu,
                 pickable=True):

        # Initiates the super class.
        pygame.sprite.Sprite.__init__(self)

        self.__full_icon = pygame.image.load(PATH_ITEMS + icon)
        self.icon = pygame.Surface((self.__full_icon.get_width() // 2,
                                     self.__full_icon.get_height()))
        self.icon.set_colorkey(GREEN)

        self.image = pygame.image.load(PATH_ITEMS + image)
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()

        self.name = name
        self.description = description
        self.contextMenu = context_menu
        self.pickable = pickable

        self.reset()

    def reset(self):
        self.icon.blit(self.__full_icon, (0, 0),
                       (0, 0,
                        self.__full_icon.get_width() // 2,
                        self.__full_icon.get_height()))

    def select(self):
        self.icon.blit(self.__full_icon, (0, 0),
                       (self.__full_icon.get_width() // 2, 0,
                        self.__full_icon.get_width() // 2,
                        self.__full_icon.get_height()))


class Jewel(Item):

    def __init__(self):
        buttons = []
        buttons.append(menus.Button("context_button.bmp", "Remove"))
        buttons.append(menus.Button("context_button.bmp", "Cancel",
                                    action="actions.cancel_menu()"))

        context_menu = menus.ContextMenu("context_menu.png", buttons)

        super(Jewel, self).__init__("Jewel",
                                    "",
                                    "jewel.bmp",
                                    "jewel_icon.bmp",
                                    context_menu)


class UsableItem(Item):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, description, image, icon):
        buttons = []
        buttons.append(menus.Button("context_button.bmp", "Use",
                                    action="actions.use_item(globals_.player_unit.inventory.items[globals_.current_window[1].selected - 1])"))
        buttons.append(menus.Button("context_button.bmp", "Remove"))
        buttons.append(menus.Button("context_button.bmp", "Cancel",
                                    action="actions.cancel_menu()"))

        context_menu = menus.ContextMenu("context_menu.png", buttons)

        super(UsableItem, self).__init__(name, description, image, icon,
                                         context_menu)

    @abstractmethod
    def applyEffects(self, unit):
        raise NotImplementedError()


class Medicine(UsableItem):

    def __init__(self):
        super(Medicine, self).__init__("Medicine",
                                       "",
                                       "hp_potion.bmp",
                                       "hp_potion_icon.bmp")

    def applyEffects(self, unit):
        if unit.health + unit.health * 0.25 >= 100:
            unit.health = 100
        else:
            unit.health = 100
