from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, overload

from RPGGame.abstract.AbstractBehaviorHandler import AbstractBehaviorHandler
from RPGGame.Enemy import Enemy
from RPGGame.Item import Weapon
from RPGGame.Vector import RectVector, Vector

if TYPE_CHECKING:
    from typing import Any, Callable, List, Union

    from RPGGame.abstract.AbstractGameState import AbstractGameState
    from RPGGame.Item import Item


class Behavior(NamedTuple):
    t_pos: Union[Vector, RectVector]
    t_map: Vector
    handler: Callable[..., None]
    data: List[Any]
    type: str
    once: bool = False


class BehaviorHandler(AbstractBehaviorHandler):
    def __init__(self):
        self._behaviors = [
            Behavior(
                RectVector(6, 1, 9, 1),
                Vector(0, 0),
                self._display_message,
                [
                    """Welcome hero. Go to the trader's home,
there is some equipment for you there.""", 0
                ],
                'message',
            ),
            Behavior(
                RectVector(18, 4, 23, 4),
                Vector(0, 0),
                self._display_message,
                [
                    """There is some gear and money in the bottom right
of my house. Take it if you wish.""", 0
                ],
                'message',
            ),
            Behavior(
                Vector(25, 6),
                Vector(0, 0),
                self._add_to_inventory,
                [Weapon.Broadsword()],
                'pickup',
                True,
            ),
            Behavior(
                RectVector(66, 1, 67, 1),
                Vector(1, 0),
                self._start_fight,
                [Enemy.Zombie()],
                'fight',
            ),
        ]

    def _add_to_inventory(self, state: AbstractGameState,
                          *items: Item) -> None:
        state.player.inventory.extend(items)
        self._display_message(
            state, 'You picked up ' + ', '.join(map(str, items)) + '.', 4)

    def _start_fight(self, state: AbstractGameState, enemy: Enemy) -> None:
        state.gameplay_state = 'fight'
        state.target = enemy

    @overload
    def _display_message(self, state: AbstractGameState, message: str):
        ...

    @overload
    def _display_message(self, state: AbstractGameState, message: str,
                         message_timeout: int):
        ...

    def _display_message(self, state: AbstractGameState, message: str,
                         *args: int) -> None:
        if len(args) == 0:
            if state.message_timeout == 0:
                state.message = message
        elif len(args) == 1:
            state.pending_messages.append(message)
            state.pending_message_timeouts.append(args[0])
        else:
            raise AttributeError("Incorrect amount of args.")

    def on_move_callback(self, state: AbstractGameState) -> None:
        for behavior in reversed(self._behaviors):
            if behavior.type == 'fight' and behavior.data[0].health <= 0:
                self._behaviors.remove(behavior)
            if (behavior.t_map == state.map_pos
                    and (behavior.t_pos == state.pos if isinstance(
                        behavior.t_pos, Vector) else behavior.t_pos.contains(
                            state.pos))):
                behavior.handler(state, *behavior.data)
                if behavior.once:
                    self._behaviors.remove(behavior)
