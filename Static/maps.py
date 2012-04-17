#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for maps to use in the game."""

__version__ = "0.1"

import pygame

from Main.constants import *


WIDTH, HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT


class Map(object):
    """Used to create a map to be displayed in the game.

    Parameters:

    config - a path to the config image
    textures - a path to the textures image
    zone - starting zone of the map
    """

    def __init__(self, config, textures, zone=1, name="island"):

        # TEMPORARY CODE
        interiors = [[[None, None]],
                     [[PATH_MAPS + "config2.bmp",
                       PATH_MAPS + "textures2.bmp"]]]
        # END OF TEMPORARY CODE

        self.__full_config = pygame.image.load(config)      # Full config image
        self.__full_textures = pygame.image.load(textures)  # Full textures image

        self.__interior = 0                                 # Current interior, 0 if none
        self.__interiors = interiors                        # List of lists containing images for interiors

        self.name = name
        self.config = pygame.Surface((WIDTH, HEIGHT))       # Current part of the config image
        self.textures = pygame.Surface((WIDTH, HEIGHT))     # Current part of the textures image
        self.filtered = pygame.Surface((WIDTH, HEIGHT))
        self.landscape = pygame.image.load(PATH_MAPS + "landscape.png")

        self.__zone = zone                                  # Current zone

        # Sets the total amount of zones to an attribute.
        for i in range(1, 5):
            if self.__full_config.get_width() == WIDTH * i:
                self.__zones = i ** 2
                break

        # Initializes the map's initial settings.
        self.__changeZone(self.__zone)      # Changes to the current zone.
        self.__updateEnterAreas()           # Updates the areas, to which the player may enter.

    def __changeZone(self, zone):
        """Changes the current zone to
        the one specified in the parameter.
        """

        if self.__zones == 1:
            x, y = 0, 0
        elif self.__zones == 4:
            if zone in (1, 2):
                x, y = WIDTH * (zone - 1), 0
            else:
                x, y = WIDTH * (zone - 3), HEIGHT
        elif self.__zones == 9:
            if zone in (1, 2, 3):
                x, y = WIDTH * (zone - 1), 0
            elif zone in (4, 5, 6):
                x, y = WIDTH * (zone - 4), HEIGHT
            elif zone in (7, 8, 9):
                x, y = WIDTH * (zone - 7), HEIGHT * 2
        elif self.__zones == 16:
            if zone in (1, 2, 3, 4):
                x, y = WIDTH * (zone - 1), 0
            elif zone in (5, 6, 7, 8):
                x, y = WIDTH * (zone - 5), HEIGHT
            elif zone in (9, 10, 11, 12):
                x, y = WIDTH * (zone - 9), HEIGHT * 2
            elif zone in (13, 14, 15, 16):
                x, y = WIDTH * (zone - 13), HEIGHT * 3
        if zone in range(1, self.__zones + 1):
            # Changes the current part of the config image.
            self.config.blit(self.__full_config, (0, 0),
                             (x, y, WIDTH, HEIGHT))

            # Changes the current part of the textures image.
            self.textures.blit(self.__full_textures, (0, 0),
                               (x, y, WIDTH, HEIGHT))

            self.__updateFiltered()

            # Changes the current zone.
            self.__zone = zone

    def __updateEnterAreas(self):
        """Updates the areas to which the player may enter."""

        self.areas = []     # List of lists containing the areas to which the player may enter

        x, y = 0, 752       # Coordinates used to determine the areas
        counter = 0         # Area's number

        while True:
            if self.config.get_at((x + 1, y)) == RED:
                counter += 1

                if self.config.get_at((x + 33, y)) == RED:
                    width = 48
                elif self.config.get_at((x + 17, y)) == RED:
                    width = 32
                else:
                    width = 16

                self.areas.append([pygame.Rect((x, y), (width, 16)),
                                   counter])
                x += width
            elif y == 0:
                break
            else:
                if x == 1008:
                    x = 0
                    y -= 16
                else:
                    x += 16

    def __updateFiltered(self):
        """Updates the filtered version of the map's textures."""

        self.filtered.blit(self.textures, (0, 0),
                            (0, 0, WIDTH, HEIGHT))

        filter_mask = pygame.image.load(PATH_MAPS + "filter_mask.png")

        filter_ = pygame.Surface((WIDTH, HEIGHT))
        filter_.blit(filter_mask, (0, 0),
                     (0, 0, WIDTH, HEIGHT))
        filter_.set_alpha(99)
        self.filtered.blit(filter_, (0, 0),
                           (0, 0, WIDTH, HEIGHT))

    @property
    def interior(self):
        """Returns the current interior."""

        return self.__interior

    @interior.setter
    def interior(self, number):
        """Sets a new interior."""

        if number == 0:
            self.__changeZone(self.__zone)
        else:
            config = \
            pygame.image.load(self.__interiors[self.__zone - 1][number - 1][0])

            textures = \
            pygame.image.load(self.__interiors[self.__zone - 1][number - 1][1])

            self.config.blit(config, (0, 0),
                             (0, 0, WIDTH, HEIGHT))
            self.textures.blit(textures, (0, 0),
                               (0, 0, WIDTH, HEIGHT))

        self.__updateFiltered()

        # Updates the interior attribute.
        self.__interior = number

        # Updates the areas to which the player may enter.
        self.__updateEnterAreas()

    @property
    def zone(self):
        """Returns the current zone."""

        return self.__zone

    @zone.setter
    def zone(self, zone):
        """Sets a new zone."""

        # Changes the current zone.
        self.__changeZone(zone)

        # Updates the areas to which the player may enter.
        self.__updateEnterAreas()

    @property
    def zones(self):
        """Returns the amount of all the zones."""

        return self.__zones
