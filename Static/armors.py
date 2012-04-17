#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains classes for armors to use in the game."""


class Armor(object):

    def __init__(self, name, description, defense, condition=100):

        self.name = name
        self.description = description
        self.defense = 0

        self.__condition = condition
        self.__initialDefense = defense

        self.condition = condition

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, condition):
        self.__condition = condition
        self.defense = (self.__initialDefense * self.__condition) // 100
