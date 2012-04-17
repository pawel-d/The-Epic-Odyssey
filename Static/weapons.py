#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for weapons to use in the game."""
from abc import ABCMeta, abstractmethod

import pygame
from pygame.locals import *

from Main.constants import *


class Weapon(pygame.sprite.Sprite):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, image, icon, battle_image, description,\
                 attack_rate):

        self.name = name
        self.description = description
        self.__attack_rate = attack_rate

        self.image = pygame.image.load(PATH_ITEMS + image)
        self.rect = self.image.get_rect()
        self.icon = pygame.image.load(PATH_ITEMS + icon)
        self.battle_image = pygame.image.load(PATH_ITEMS + battle_image)
