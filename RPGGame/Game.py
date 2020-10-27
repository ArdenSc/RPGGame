from __future__ import annotations

from copy import deepcopy
from os import system
from random import choice
from sys import platform
from typing import TYPE_CHECKING, overload

from RPGGame.Exceptions import *
from RPGGame.GameState import Vector
from RPGGame.Item import Heal, Weapon

if TYPE_CHECKING:
    from typing import Any, List

    from typing_extensions import Literal

    from RPGGame.abstract.AbstractBehaviorHandler import \
        AbstractBehaviorHandler
    from RPGGame.abstract.AbstractGameState import AbstractGameState
    from RPGGame.abstract.AbstractMenu import AbstractMenu
    from RPGGame.MapSegment import MapSegment


def _terminal_resize(columns: int, lines: int):
    """Internal function that resizes the terminal to the specific dimensions.

    Args:
        columns: The amount of vertical columns.
        lines: The amount of horizontal lines.
    """
    if platform == 'win32':
        system(f"mode con: cols={columns} lines={lines}")
    else:
        system(f"resize -s {columns} {lines}")


def _invalid_register_type():
    """Internal function to be used as a default value for the
    register_switch in the Game class.
    """
    raise AttributeError("Invalid type registered to Game object.")


def _invalid_gameplay_state():
    """Internal function to be used as a default value for the
    state_switch in the Game class.
    """
    raise AttributeError("Invalid gameplay state.")


class Game:
    """A semi-modular framework for a terminal rpg game.

    Requires at least maps and a menu, add them using the register method.
    """
    def __init__(self, state: AbstractGameState) -> None:
        """Creates an instance of the game framework.

        Args:
            state: An instance of a class that inherits AbstractGameState.
        """
        self._starting_state = state
        self._state = deepcopy(self._starting_state)
        self._register_switch = {
            "menu": self._register_menu,
            "maps": self._register_maps,
            "behaviors": self._register_behaviors,
        }
        self._dir_switch = {
            0: Vector.North(),
            1: Vector.East(),
            2: Vector.South(),
            3: Vector.West(),
        }
        self._state_switch = {
            "start": self._mainmenu,
            "navigate": self._navigate,
            "fight": self._fight,
        }

    def _register_menu(self, menu: AbstractMenu) -> None:
        """Internal method for registering a menu"""
        self._menu = menu

    def _register_maps(self, maps: List[List[MapSegment]],
                       map_names: List[List[str]]) -> None:
        """Internal method for registering maps"""
        self._starting_maps = maps
        self._starting_map_names = map_names
        self._state.maps = deepcopy(self._starting_maps)
        self._state.map_names = deepcopy(self._starting_map_names)

    def _register_behaviors(self, handler: AbstractBehaviorHandler) -> None:
        """Internal method for registering a behavior handler."""
        self._starting_behaviors = handler
        self._behaviors = deepcopy(self._starting_behaviors)

    @overload
    def register(self, type: Literal['menu'], menu: AbstractMenu) -> None:
        """Registers a menu handler to the game.

        Args:
            type: Must be a string of value 'menu'.
            menu: An instance of an AbstractMenu subclass.
        """
        ...

    @overload
    def register(self, type: Literal['maps'], maps: List[List[MapSegment]],
                 map_names: List[List[str]]) -> None:
        """Registers maps to the game.

        Args:
            type: Must be a string of value 'maps'.
            maps: 2D list of MapSegments.
        """
        ...

    @overload
    def register(self, type: Literal['behaviors'],
                 handler: AbstractBehaviorHandler) -> None:
        """Registers a behavior handler to the game.

        Args:
            type: Must be a string of value 'behaviors'.
            handler: A subclass of AbstractBehaviorHandler.
        """
        ...

    def register(self, type: str, *args: Any) -> None:
        """Base method for registering maps or a handler.

        See overloads for details specific to each registerable item.
        """
        self._register_switch.get(type, _invalid_register_type)(*args)

    def _navigate(self) -> None:
        """Internal method for calling the navigation menu."""
        dir = self._menu.navigate(self._state)
        self._move(self._dir_switch[dir])
        self._behaviors.on_move_callback(self._state)

    def _mainmenu(self) -> None:
        """Internal method for calling the title menu."""
        self._menu.mainmenu()
        self._state.gameplay_state = 'navigate'

    def _end_fight(self) -> None:
        """Internal method for ending an active fight."""
        self._state.fight_state = None
        self._state.gameplay_state = 'navigate'

    def _fight(self) -> None:
        """Internal method for handling an active fight."""
        if not self._state.fight_state:
            self._state.fight_state = {
                'menu': 'action',
                'run_failed': False,
                'amt_options': 3,
            }
        option = self._menu.fight(self._state)
        if self._state.fight_state['menu'] == 'action':
            if option == 0:
                self._state.fight_state['menu'] = 'attack'
                self._state.fight_state['amt_options'] = sum(
                    1 for x in self._state.player.inventory
                    if isinstance(x, Weapon)) + 1
            elif option == 1:
                self._state.fight_state['menu'] = 'heal'
                self._state.fight_state['amt_options'] = sum(
                    1 for x in self._state.player.inventory
                    if isinstance(x, Heal)) + 1
            elif choice((True, False)):
                self._end_fight()
                self._state.pending_messages.append('You got away.')
                self._state.pending_message_timeouts.append(4)
            else:
                self._state.fight_state['run_failed'] = True
                self._state.fight_state['amt_options'] = 2
                self._state.message = "You couldn't get away."
        elif self._state.fight_state['menu'] == 'attack':
            if option == 0:
                self._state.fight_state['menu'] = 'action'
                self._state.fight_state[
                    'amt_options'] = 2 if self._state.fight_state[
                        'run_failed'] else 3
            else:
                option -= 1
                weapon = [
                    x for x in self._state.player.inventory
                    if isinstance(x, Weapon)
                ][option]
                damage_in = self._state.target.damage
                damage_in -= self._state.player.armor
                self._state.player.health -= damage_in
                damage_out = weapon.damage
                self._state.target.health -= damage_out
                self._state.message = f"""\
You did {damage_out} dmg to the \
{self._state.target.name}, it did {damage_in} to you.\
"""
                if self._state.player.health <= 0:
                    raise LoseGame
                if self._state.target.health <= 0:
                    self._state.player.inventory.extend(
                        self._state.target.drops)
                    self._state.pending_messages.append(
                        f"You killed the {self._state.target.name}! " +
                        'It dropped ' +
                        (', '.join(x.name
                                   for x in self._state.target.drops) if self.
                         _state.target.drops else 'nothing') + '.')
                    self._state.pending_message_timeouts.append(4)
                    self._state.fight_state = None
                    self._state.gameplay_state = 'navigate'
        elif self._state.fight_state['menu'] == 'heal':
            if option == 0:
                self._state.fight_state['menu'] = 'action'
                self._state.fight_state[
                    'amt_options'] = 2 if self._state.fight_state[
                        'run_failed'] else 3
            else:
                option -= 1
                heal = [
                    x for x in self._state.player.inventory
                    if isinstance(x, Heal)
                ][option]
                self._state.player.health += heal.health
                self._state.message = f"You restored {heal.health} health."
                heal.used = True
                self._state.fight_state['amt_options'] = sum(
                    1 for x in self._state.player.inventory
                    if isinstance(x, Heal)) + 1

    def _move(self, movement: Vector):
        """Internal method for moving the player."""
        old_pos = deepcopy(self._state.pos)
        self._state.pos += movement
        x, y = self._state.pos
        mx, my = self._state.map_pos
        if x < 0:
            if mx >= 1:
                self._state.map_pos += Vector(-1, 0)
                self._state.pos[0] = self._state.get_map(mx - 1, my).width - 1
            else:
                self.pos = old_pos
        elif x >= self._state.get_map(mx, my).width:
            if mx + 1 < len(self._state.maps[0]):
                self._state.map_pos += Vector(1, 0)
                self._state.pos[0] = 0
            else:
                self._state.pos = old_pos
        if y < 0:
            if my >= 1:
                self._state.map_pos += Vector(0, -1)
                self._state.pos[1] = self._state.get_map(mx, my - 1).height - 1
            else:
                self._state.pos = old_pos
        elif y >= self._state.get_map(mx, my).height:
            if my + 1 < len(self._state.maps):
                self._state.map_pos += Vector(0, 1)
                self._state.pos[1] = 0
            else:
                self._state.pos = old_pos

        if self._state.get_map(*self._state.map_pos).get(
                *self._state.pos) in ('▀', '▌', '▁', '▔', '▄', '█', '▛', '▜',
                                      '▙', '▟', '▐'):
            self._state.pos = old_pos

    def _reset(self) -> None:
        """Internal method for resetting the game state for replayability."""
        self._state = deepcopy(self._starting_state)
        self._state.maps = deepcopy(self._starting_maps)
        self._state.map_names = deepcopy(self._starting_map_names)
        self._behaviors = deepcopy(self._starting_behaviors)


    def run(self) -> None:
        """Starts the game.

        All requirements must have been registered before calling this method.
        """
        if not hasattr(self, '_menu'):
            raise AttributeError("A Menu is required to run the game.")
        if not hasattr(self._state, 'maps'):
            raise AttributeError("Maps are required to run the game.")
        if not hasattr(self, '_behaviors'):
            raise AttributeError("Behaviors are required to run the game.")
        _terminal_resize(135, 35)
        while True:
            try:
                self._state_switch.get(self._state.gameplay_state,
                                       _invalid_gameplay_state)()
            except (StopGame, WinGame, LoseGame) as e:
                if isinstance(e, StopGame):
                    break
                elif isinstance(e, WinGame):
                    self._menu.winmenu()
                else:
                    self._menu.losemenu()
                self._reset()
