#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved

"""This module contains procedures
to be used when dealing with CPU units.
"""

__version__ = "0.1"

# Imports modules from local packages
import Main.globals as globals_
import Quests.scripting as scripting
from Main.constants import *


def __move_units():
    """Moves CPU units."""

    if len(globals_.units_to_move) > 0:
        for un in globals_.units_to_move:
            if un[2] == UP and un[0].rect.y > un[3] - un[1]:
                if un[0].rect.y - un[0].speed >= un[3] - un[1]:
                    un[0].move(UP)
                else:
                    if scripting._possible_to_move(un[0], un[0].speed, UP):
                        un[0].move(UP)
            elif un[2] == DOWN and un[0].rect.y + un[0].rect.height \
            < un[0].rect.height + un[3] + un[1]:
                if un[0].rect.y + un[0].rect.height + un[0].speed \
                <= un[0].rect.height + un[3] + un[1]:
                    un[0].move(DOWN)
                else:
                    if scripting._possible_to_move(un[0], un[0].speed, DOWN):
                        un[0].move(DOWN)
            elif un[2] == LEFT and un[0].rect.x > un[3] - un[1]:
                if un[0].rect.x - un[0].speed >= un[3] - un[1]:
                    un[0].move(LEFT)
                else:
                    if scripting._possible_to_move(un[0], un[0].speed, LEFT):
                        un[0].move(LEFT)
            elif un[2] == RIGHT and un[0].rect.x + un[0].rect.width \
            < un[0].rect.width + un[3] + un[1]:
                if un[0].rect.x + un[0].rect.width + un[0].speed <= \
                un[0].rect.width + un[3] + un[1]:
                    un[0].move(RIGHT)
                else:
                    if scripting._possible_to_move(un[0], un[0].speed, RIGHT):
                        un[0].move(RIGHT)
            else:
                un[0].stop()
                globals_.units_to_move.remove(un)


def manage_events():
    if len(globals_.events) > 0:
        for event in globals_.events:
            exec(event)


def manage_units():
    """Manages all of the CPU units."""

    __move_units()

if __name__ == "__main__":
    class DirectRunError(Exception):
        pass

    raise DirectRunError("This module cannot be run directly.")
