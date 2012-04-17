#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved.

"""This module contains functions and procedures
to be used when scripting quests.
"""

__version__ = "0.1"

import copy
import traceback

import pygame
from pygame.locals import *

# Imports modules from local packages.
import Interface.windows as windows
import Main.globals as globals_
import NonStatic.characters as characters
import NonStatic.creatures as creatures
import Static.armors as armors
import Static.maps as maps
import Static.items as items
import Static.weapons as weapons
from Main.constants import *


def __check_if_collide(object_, distance, direction):
    """Checks whether the specified object will collide
    with any of the objects in the global variables
    if traveled a given distance.

    Parameters:

    'object_' - one of the game's object type (i.e. Character, Creature etc.)
    'distance' - amount of pixels by which the object will be moved
    'direction' - side towards which the object will be moved
    """

    # Creates a new instance of the object.
    tmp = copy.deepcopy(object_)

    # Simulates the movement of the object.
    if direction == UP:
        tmp.rect.y -= distance
    elif direction == DOWN:
        tmp.rect.y += distance
    elif direction == LEFT:
        tmp.rect.x -= distance
    elif direction == RIGHT:
        tmp.rect.x += distance

    # Checks whether the object will collide with any of the in-game objects.
    if len(globals_.objects_in_game) > 0:
        for obj in globals_.objects_in_game.sprites():
            if pygame.sprite.collide_rect(tmp, obj):
                return True

    # Checks whether the object will collide with any of the in-game units.
    if len(globals_.units_in_game) > 0:
        for un in globals_.units_in_game.sprites():
            if pygame.sprite.collide_rect(tmp, un):
                return True

    # Returns False if the object won't collide with anything.
    return False


def _can_enter(unit):
    """Checks whether the specified unit
    is within an area of the map from which it can enter a building.

    Parameters:

    'unit' - one of the game's units type (i.e. Character, Creature)
    """

    for area in globals_.current_map.areas:
        if pygame.Rect.colliderect(unit.rect, area[0]):
            # Returns the number of the area if possible to enter.
            return area[1]

    # Returns False if impossible to enter.
    return False


def _can_pick_up():
    player = copy.deepcopy(globals_.player_unit)

    for obj in globals_.objects_in_game.sprites():
        player.rect.x += 1
        if pygame.sprite.collide_rect(player, obj):
            if player.direction == RIGHT:
                if obj.pickable:
                    return obj
                else:
                    break
        player.rect.x -= 2
        if pygame.sprite.collide_rect(player, obj):
            if player.direction == LEFT:
                if obj.pickable:
                    return obj
                else:
                    break
        player.rect.x += 1
        player.rect.y -= 1
        if pygame.sprite.collide_rect(player, obj):
            if player.direction == UP:
                if obj.pickable:
                    return obj
                else:
                    break
        player.rect.y += 2
        if pygame.sprite.collide_rect(player, obj):
            if player.direction == DOWN:
                if obj.pickable:
                    return obj
                else:
                    break


def _possible_to_move(unit, distance, direction, map_=None):
    """Checks whether it will be possible to move a specified unit
    if it travels a specified distance.

    Parameters:

    'unit' - one of the game's units type (i.e. Character, Creature)
    'distance' - amount of pixels by which the unit will be moved
    'direction' - side towards the which the unit will be moved
    'map_' - the Map object on which the unit is
    """

    if map_ is None:
        map_ = globals_.current_map

    # Unit's top side
    top = (unit.rect.x,
           unit.rect.x + unit.rect.width,
           unit.rect.y - distance,
           unit.rect.y)

    # Unit's bottom side
    bottom = (unit.rect.x,
              unit.rect.x + unit.rect.width,
              unit.rect.y + unit.rect.height,
              unit.rect.y + unit.rect.height + distance)

    # Unit's left side
    left = (unit.rect.y,
            unit.rect.y + unit.rect.height,
            unit.rect.x - distance,
            unit.rect.x)

    # Unit's right side
    right = (unit.rect.y,
             unit.rect.y + unit.rect.height,
             unit.rect.x + unit.rect.width,
             unit.rect.x + unit.rect.width + distance)

    # Checks if the unit collides with any of the in-game objects and units.
    if __check_if_collide(unit, distance, direction):
        return False
    else:
        # Checks if the unit will overlap any of the solid objects on the map.
        try:

            if direction == UP:
                for x in range(top[0], top[1]):
                    for y in range(top[2], top[3]):
                        if map_.config.get_at((x, y)) == BLUE:
                            if map_.config.get_at((x, y + \
                                        int(unit.rect.height // 1.5) - \
                                        distance)) == BLUE:
                                return False
                return True

            elif direction == DOWN:
                for x in range(bottom[0], bottom[1]):
                    for y in range(bottom[2], bottom[3]):
                        if map_.config.get_at((x, y)) == BLUE:
                            if map_.config.get_at((x, y + \
                                        int(unit.rect.height // 1.5))) == BLUE:
                                return False
                return True

            elif direction == LEFT:
                for y in range(left[0], left[1]):
                    for x in range(left[2], left[3]):
                        if map_.config.get_at((x, y)) == BLUE:
                            if map_.config.get_at((x, y + \
                                        int(unit.rect.height // 1.5))) == BLUE:
                                return False
                return True

            elif direction == RIGHT:
                for y in range(right[0], right[1]):
                    for x in range(right[2], right[3]):
                        if map_.config.get_at((x, y)) == BLUE:
                            if map_.config.get_at((x, y + \
                                        int(unit.rect.height // 1.5))) == BLUE:
                                return False
                return True

        except IndexError:
            return False


def attack_character(character1, character2):
    try:
        raise NotImplementedError("error! 'attack_character' function \
                                   has not been implemented yet")
    except NotImplementedError as err:
        windows.show_error(err, traceback.extract_stack()[-1])


def can_move(unit, distance, direction):
    """Checks whether a unit can
    move a specified distance in a given direction.

    Parameters:

    'unit' - one of the game's unit types (i.e. Character, Creature etc.)
    'distance' - amount of pixels by which the object will be moved
    'direction' - side towards which the object will be moved
    """

    try:
        if not isinstance(unit, characters.Character) \
        and not isinstance(unit, creatures.Creature):
            raise TypeError("error! invalid 'unit' type")
        elif not type(distance) is int:
            raise TypeError("error! 'distance' parameter must be an integer")
        elif not direction in (8, 2, 4, 6):
            raise Exception("error! invalid 'direction' parameter")
        elif not unit in globals_.units_in_game:
            raise Exception("error! the unit has to be \
                            placed on the map.")
    except (Exception, TypeError) as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if _possible_to_move(unit, distance, direction):
            return True
        else:
            return False


def create_human(name, spritesheet,
                 armor=None, inventory=None, weapon=None):
    """Creates a new 'Human' object and returns a reference to its class.

    Parameters:

    'name' - name of the unit
    'spritesheet' - name of the file containing character's animations
    'armor' - Armor object to be used by the unit
    'inventory' - Inventory object to be used by the unit
    'weapon' - Weapon object to be used by the unit
    """

    try:
        if not isinstance(name, str) or not len(name) <= 15:
            raise Exception("error! invalid 'name' parameter")
        elif not isinstance(spritesheet, str):
            raise Exception("error! invalid 'spritesheet' parameter")
        elif not armor is None and not isinstance(armor, armors.Armor):
            raise Exception("error! invalid 'armor' parameter")
        elif not inventory is None and not isinstance(inventory,
                                                      windows.Inventory):
            raise Exception("error! invalid 'inventory' parameter")
        elif not weapon is None and not isinstance(weapon, weapons.Weapon):
            raise Exception("error! invalid 'weapon' parameter")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        return characters.Human(name, PATH_CHARACTERS + spritesheet,
                                armor, inventory, weapon)


def create_map(name, config_path, textures_path, zone):
    """Creates a new 'Map' object and returns a reference to its class.

    Parameters:

    'name' - name of the map
    'config_path' - name of the config image of the map
    'textures_parh' - name of the textures image of the map
    'zone' - map's initial zone
    """

    try:
        if not isinstance(name, str):
            raise TypeError("error! 'name' parameter must be a string")
        elif not isinstance(config_path, str):
            raise TypeError("error! 'config_path' parameter must be a string")
        elif not isinstance(textures_path, str):
            raise TypeError("error! 'textures_path' parameter must be a string")
        elif not type(zone) is int:
            raise TypeError("error! 'zone' parameter must be an integer")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        return maps.Map(PATH_MAPS + config_path,
                        PATH_MAPS + textures_path,
                        zone)


def create_olympian(name, spritesheet):
    try:
        raise NotImplementedError("error! 'create_olympian' function \
                                   has not been implemented yet")
    except NotImplementedError as err:
        windows.show_error(err, traceback.extract_stack()[-1])


def create_titan(name, spritesheet):
    try:
        raise NotImplementedError("error! 'create_titan' function \
                                   has not been implemented yet")
    except NotImplementedError as err:
        windows.show_error(err, traceback.extract_stack()[-1])


def event(code):
    """Adds an event to the game's stack.

    Parameters

    'code' - Python code to be executed
    """

    try:
        if not type(code) is str:
            raise TypeError("error! 'code' parameter must be a string")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        globals_.events.append(code)


def load_human(name):
    """Loads a Human from data and returns a reference to is class.

    Parameters

    'name' - name of the unit, specified in the data
    """

    class FileError(Exception):
        pass

    class UnitNameError(Exception):
        pass

    try:
        if not type(name) is str or len(name) == 0:
            raise TypeError("error! incorrect 'name' parameter")

        unit = None
        for first in globals_.game_files:
            if first == "Human":
                for second in globals_.game_files[first]:
                    if second.get("name") == name:
                        unit = second
                        break
                else:
                    raise UnitNameError("error! '" + name + "' does not exist")
                break
        else:
            raise FileError("error! 'data1.epic' file is corrupted")
    except (FileError, TypeError, UnitNameError) as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        human = characters.Human(unit.get("name"),
                                 PATH_CHARACTERS + unit.get("image"),
                                 None,
                                 None,
                                 unit.get("weapon"))
        human.defense = unit.get("defense")
        human.speed = unit.get("speed")
        human.agility = unit.get("agility")
        human.skills = unit.get("skills")

        return human


def load_map(name):
    """Loads a map from data and returns a reference to its class.

    Parameters:

    'name' - name of the map, specified in the data
    """

    class FileError(Exception):
        pass

    class UnitNameError(Exception):
        pass

    try:
        if not type(name) is str or len(name) == 0:
            raise TypeError("error! incorrect 'name' parameter")

        tmp_map = None
        for first in globals_.game_files:
            if first == "Map":
                for second in globals_.game_files[first]:
                    if second.get("name") == name:
                        tmp_map = second
                        break
                else:
                    raise UnitNameError("error! '" + name + "' does not exist")
                break
        else:
            raise FileError("error! 'data1.epic' file is corrupted")
    except (FileError, TypeError, UnitNameError) as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        map_ = maps.Map(PATH_MAPS + tmp_map.get("config"),
                        PATH_MAPS + tmp_map.get("textures"),
                        tmp_map.get("zone"))

        return map_


def load_olympian(name):
    """Loads an Olympian from data and returns a reference to is class.

    Parameters

    'name' - name of the unit, specified in the data
    """

    class FileError(Exception):
        pass

    class UnitNameError(Exception):
        pass

    try:
        if not type(name) is str or len(name) == 0:
            raise TypeError("error! incorrect 'name' parameter")

        unit = None
        for first in globals_.game_files:
            if first == "Olympian":
                for second in globals_.game_files[first]:
                    if second.get("name") == name:
                        unit = second
                        break
                else:
                    raise UnitNameError("error! '" + name + "' does not exist")
                break
        else:
            raise FileError("error! 'data1.epic' file is corrupted")
    except (FileError, TypeError, UnitNameError) as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        olympian = characters.Olympian(unit.get("name"),
                                       PATH_CHARACTERS + unit.get("image"),
                                       unit.get("weapon"))
        olympian.defense = unit.get("defense")
        olympian.speed = unit.get("speed")
        olympian.agility = unit.get("agility")
        olympian.skills = unit.get("skills")

        return olympian


def load_titan(name):
    """Loads a Titan from data and returns a reference to is class.

    Parameters

    'name' - name of the unit, specified in the data
    """

    class FileError(Exception):
        pass

    class UnitNameError(Exception):
        pass

    try:
        if not type(name) is str or len(name) == 0:
            raise TypeError("error! incorrect 'name' parameter")

        unit = None
        for first in globals_.game_files:
            if first == "Titan":
                for second in globals_.game_files[first]:
                    if second.get("name") == name:
                        unit = second
                        break
                else:
                    raise UnitNameError("error! '" + name + "' does not exist")
                break
        else:
            raise FileError("error! 'data1.epic' file is corrupted")
    except (FileError, TypeError, UnitNameError) as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        titan = characters.Olympian(unit.get("name"),
                                    PATH_CHARACTERS + unit.get("image"),
                                    unit.get("weapon"))
        titan.defense = unit.get("defense")
        titan.speed = unit.get("speed")
        titan.agility = unit.get("agility")
        titan.skills = unit.get("skills")

        return titan


def move_unit(unit, distance, direction):
    """Moves a unit a specified distance in a given direction.

    Parameters:

    'unit' - one of the game's unit types (i.e. Character, Creature etc.)
    'distance' - amount of pixels by which the object will be moved
    'direction' - side towards which the object will be moved
    """

    try:
        if not isinstance(unit, characters.Character) \
        and not isinstance(unit, creatures.Creature):
            raise Exception("error! invalid 'unit' parameter")
        elif not distance or not type(distance) is int:
            raise Exception("error! distance parameter must be an integer")
        elif not direction or not type(direction) is int:
            raise Exception("error! direction parameter must be an integer")
        elif not unit in globals_.units_in_game:
            raise Exception("error! the unit is not on the map")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if _possible_to_move(unit, distance, direction):
            if direction == UP or direction == DOWN:
                globals_.units_to_move.append([unit, distance, direction,
                                               unit.rect.y])
            elif direction == LEFT or direction == RIGHT:
                globals_.units_to_move.append([unit, distance, direction,
                                               unit.rect.x])


def move_unit_steps(unit, steps, direction):
    """Moves a unit a specified amount of steps in a given direction.

    Parameters:

    'unit' - one of the game's unit types (i.e. Character, Creature etc.)
    'distance' - amount of steps by which the object will be moved
    'direction' - side towards which the object will be moved
    """

    try:
        if not isinstance(unit, characters.Character) \
        and not isinstance(unit, creatures.Creature):
            raise Exception("error! invalid 'unit' parameter")
        elif not steps or not type(steps) is int:
            raise Exception("error! 'steps' parameter must be an integer")
        elif not direction or not type(direction) is int:
            raise Exception("error! 'direction' parameter must be an integer")
        elif not unit in globals_.units_in_game:
            raise Exception("error! the unit is not on the map")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if _possible_to_move(unit, steps * unit.speed, direction):
            if direction == UP or direction == DOWN:
                globals_.units_to_move.append([unit, steps * unit.speed,
                                               direction, unit.rect.y])
            elif direction == LEFT or direction == RIGHT:
                globals_.units_to_move.append([unit, steps * unit.speed,
                                               direction, unit.rect.x])


def place_item(item_id, x, y):
    try:
        if not item_id in ITEMS:
            raise Exception("error! incorrect 'item_id' parameter")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if item_id == MEDICINE:
            item = items.Medicine()
        elif item_id == JEWEL:
            item = items.Jewel()

        item.rect.x = x
        item.rect.y = y

        globals_.objects_in_game.add(item)


def place_unit(unit, x, y):
    """Places a unit at the specified coordinates on the map.

    Parameters:

    'unit' - one of the game's units
    'x' - x-coordinate on the map
    'y' - y-coordinate on the map
    """

    try:
        if not isinstance(unit, characters.Character) \
        and not isinstance(unit, creatures.Creature):
            raise Exception("error! invalid 'unit' parameter")
        elif not type(x) is int or not x in range(0, 1025 - unit.rect.width):
            raise Exception("error! invalid 'x' parameter")
        elif not type(y) is int or not y in range(0, 769 - unit.rect.height):
            raise Exception("error! invalid 'y' parameter")
        elif unit in globals_.units_in_game:
            raise Exception("error! the unit is already in game")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        unit.rect.x = x
        unit.rect.y = y
        globals_.units_in_game.add(unit)


def remove_item(item):
    for i, j in enumerate(globals_.objects_in_game.sprites()):
        if j is item:
            globals_.items_placement[i] = False
            globals_.objects_in_game.remove(item)


def say(character, text_id):
    try:
        raise NotImplementedError("error! 'say' function \
                                   has not been implemented yet")
    except NotImplementedError as err:
        windows.show_error(err, traceback.extract_stack()[-1])


def set_background_sound(sound):
    """Sets a background sound to be played during the game.

    Parameters:

    'sound' - name of the song to be played
    """

    try:
        if not isinstance(sound, str):
            raise TypeError("error! 'music' parameter must be a string")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if not PATH_MUSIC + sound == globals_.current_bg_sound[0]:
            globals_.current_bg_sound[0] = PATH_MUSIC + sound
            globals_.current_bg_sound[1] = True


def set_map(map_):
    """Sets a map to be currently displayed on the screen.

    Parameters:

    "map_" - a Map object
    """

    try:
        if not isinstance(map_, maps.Map):
            raise Exception("error! invalid 'map_' parameter")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        globals_.current_map = map_


def set_music(music):
    """Sets the current music to be played during the game.

    Parameters:

    'music' - name of the song to be played
    """

    try:
        if not isinstance(music, str):
            raise TypeError("error! 'music' parameter must be a string")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if not PATH_MUSIC + music == globals_.current_music[0]:
            globals_.current_music[0] = PATH_MUSIC + music
            globals_.current_music[1] = True


def set_player_character(character):
    """Sets a character to be controllable by the player.

    Parameters:

    'character' - one of the game's characters
    """

    try:
        if not isinstance(character, characters.Character):
            raise Exception("error! invalid 'unit' parameter")
        elif not character in globals_.units_in_game:
            raise Exception("error! given character is not placed on the map")
    except Exception as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        globals_.units_in_game.remove(character)
        globals_.player_unit = character


def turn_unit(unit, direction):
    """Turns a unit to a specified direction.

    Parameters:

    'unit' - one of the game's unit types (i.e. Character, Creature etc.)
    'direction' - side towards which the unit should turn to
    """

    try:
        if not isinstance(unit, characters.Character) \
        or not isinstance(unit, creatures.Creature):
            raise TypeError("error! incorrect 'unit' parameter")
        elif not direction or not type(direction) is int \
        or not direction in (UP, DOWN, LEFT, RIGHT):
            raise TypeError("error! incorrect 'direction' parameter")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        unit.turn(direction)


def units_in_range(unit1, unit2, range_=48):
    """Checks whether two units are in range.

    Parameters:

    'unit1' - one of the game's units
    'unit2' - one of the game's units
    'range_' - maximum distance between the units
    """

    try:
        if not isinstance(unit1, characters.Character) \
        or not isinstance(unit2, creatures.Creature):
            raise TypeError("error! invalid 'unit1' parameter")
        elif not isinstance(unit2, characters.Character) \
        or not isinstance(unit2, creatures.Creature):
            raise TypeError("error! invalid 'unit2' parameter")
    except TypeError as err:
        windows.show_error(err, traceback.extract_stack()[-1])
    else:
        if unit2.rect.x in range(unit1.rect.x - range_,
                                 unit1.rect.x + unit1.rect.width + \
                                 range_ + 1) \
        and unit2.rect.y in range(unit1.rect.y - range_,
                                  unit1.rect.y + unit1.rect.height + \
                                  range_ + 1):
            return True
        else:
            return False
