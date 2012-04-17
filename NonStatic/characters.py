#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for various types of characters
to use in the game.
"""

__version__ = "0.1"

from abc import ABCMeta, abstractmethod

import pygame

import AI.interactions as interactions
import NonStatic.abstract as abstract
import Static.armors as armors
from Main.constants import *


class Character(pygame.sprite.Sprite):
    """Abstract class used to create characters.

    Parameters:

    'name' - character's name to be used across the game
    'defense' - character's base defense
    'speed' - character's base speed
    'spritesheet' - a spritesheet image, containing animations
                    of the character
    'agility' - character's agility level
    'skills' - a list containing character's skills:
               first element for melee weapon skill,
               second element for range weapon skill
    'direction' - initial direction of the character
    'health' - initial health level of the character
    'weapon' - character's weapon
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, defense, speed, spritesheet,
                 agility=1, skills=[1, 1],
                 direction=DOWN, health=100, weapon=None, behavior=None):

        # Initiates the super class.
        pygame.sprite.Sprite.__init__(self)

        self.__spritesheet = pygame.image.load(spritesheet)
        self.direction = direction

        # Initiates the super class's properties.
        self.image = self.__init_frame()
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()

        # Initiates the rest of the class's attributes
        self.agility = agility
        self.defense = defense
        self.health = health
        self.level = 1
        self.name = name
        self.speed = speed
        self.weapon = weapon

        if behavior is None:
            self.behavior = interactions.Behavior(FRIEND, ["D1"])
        else:
            self.behavior = behavior

        self.__current_foot_movement = IDLE
        self.__frames_counter = 0

    def __animate_movement(self):
        """Animates movement of the character during the walk."""

        if self.__frames_counter in (0, 10, 20, 30):
            if self.__current_foot_movement in (IDLE, LEFT, RIGHT):
                x, y = self.__return_frame_position()
                if self.__current_foot_movement in (IDLE, RIGHT):
                    offset = self.rect.width
                    self.__current_foot_movement = LEFT
                elif self.__current_foot_movement == LEFT:
                    offset = self.rect.width * 2
                    self.__current_foot_movement = RIGHT
            self.image.blit(self.__spritesheet, (0, 0),
                            (x + offset, y, self.rect.width,
                             self.rect.height))
        elif self.__frames_counter in (5, 15, 25):
            x, y = self.__return_frame_position()
            offset = 0
            self.image.blit(self.__spritesheet, (0, 0),
                            (x + offset, y, self.rect.width,
                             self.rect.height))
        elif self.__frames_counter > 30:
            self.__frames_counter = 0

        self.__frames_counter += 1

    def __init_frame(self):
        """Returns the initial image (frame) of the character."""

        size = (self.__spritesheet.get_width() // 3,
                self.__spritesheet.get_height() // 4)
        x, y = self.__return_frame_position()

        image = pygame.Surface((size[0], size[1]))
        image.blit(self.__spritesheet, (0, 0),
                   (x, y, size[0], size[1]))

        return image

    def __restart_movement(self):
        """Restores character's animation to the idle state."""

        self.__current_foot_movement = IDLE
        self.__frames_counter = 0

    def __return_frame_position(self):
        """Returns the position of a frame on character's spritesheet."""

        size = (self.__spritesheet.get_width() // 3,
                self.__spritesheet.get_height() // 4)

        if self.direction == UP:
            x, y = 0, 0
        elif self.direction == DOWN:
            x, y = 0, 0 + size[1]
        elif self.direction == LEFT:
            x, y = 0, 0 + size[1] * 2
        elif self.direction == RIGHT:
            x, y = 0, 0 + size[1] * 3

        return x, y

    def move(self, direction=DOWN):
        """Moves character in a specified direction."""

        self.direction = direction
        self.__animate_movement()

        if self.direction == UP:
            self.rect.y -= self.speed
        elif self.direction == DOWN:
            self.rect.y += self.speed
        elif self.direction == LEFT:
            self.rect.x -= self.speed
        elif self.direction == RIGHT:
            self.rect.x += self.speed

    def stop(self):
        """Stops the current character's animation."""

        self.__frames_counter = 5
        self.__animate_movement()
        self.__restart_movement()

    def turn(self, direction):
        """Turns the character to a specified direction."""

        self.direction = direction
        self.__frames_counter = 5
        self.__animate_movement()
        self.__restart_movement()

    def use(self, item):
        """Applies the effects of the item on the character."""

        item.applyEffects(self)


class Human(Character):
    """Creates a Human-type character.

    Parameters:

    'name' - character's name to be used across the game
    'spritesheet' - a spritesheet image, containing
                    animations of the character
    'armor' - character's armor
    'inventory' - character's inventory
    'weapon' - charactter's weapon
    """

    def __init__(self, name, spritesheet,
                 armor=None, inventory=None, weapon=None):

        # Initiates the super class.
        super(Human, self).__init__(name, 5, 2, spritesheet, weapon=weapon)

        self.art_image = pygame.image.load(PATH_CHARACTERS + "art_image_hero.png")

        # Initiates the class's attributes.
        if not armor is None:
            self.armor = armor
        else:
            self.armor = armors.Armor("", "", 1000)

        if not inventory is None:
            self.inventory = inventory
        else:
            self.inventory = abstract.Inventory()


class Olympian(Character):
    """Creates an Olympian-type character.

    Parameters:

    'name' - character's name to be used across the game
    'spritesheet' - a spritesheet image, containing
                    animations of the character
    'weapon' - charactter's weapon
    """

    def __init__(self, name, spritesheet, weapon):

        # Initiates the super class.
        super(Olympian, self).__init__(name, 250, 2, spritesheet,
                                       weapon=weapon)


class Titan(Character):
    """Creates a Titan-type character.

    'name' - character's name to be used across the game
    'spritesheet' - a spritesheet image, containing
                    animations of the character
    'weapon' - charactter's weapon
    """

    def __init__(self, name, spritesheet, weapon):

        # Initiates the super class.
        super(Titan, self).__init__(name, 220, 2, spritesheet, weapon=weapon)
