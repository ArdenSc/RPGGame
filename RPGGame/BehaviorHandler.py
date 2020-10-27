from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, overload

from RPGGame.abstract.AbstractBehaviorHandler import AbstractBehaviorHandler
from RPGGame.Enemy import Enemy
from RPGGame.Item import Armor, Weapon, Heal, Item
from RPGGame.Vector import RectVector, Vector

if TYPE_CHECKING:
    from typing import Any, Callable, List, Union

    from RPGGame.abstract.AbstractGameState import AbstractGameState


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
                Vector(71, 18),
                Vector(1, 1),
                self._add_to_inventory,
                [Heal.Bandage()],
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
            Behavior(
                RectVector(71, 1, 72, 1),
                Vector(1, 0),
                self._start_fight,
                [Enemy.Skeleton()],
                'fight',
            ),
            Behavior(
                RectVector(76, 1, 77, 1),
                Vector(1, 0),
                self._start_fight,
                [Enemy.Warrior()],
                'fight',
            ),
            Behavior(RectVector(18, 4, 19, 4), Vector(1, 0), self._start_fight,
                     [Enemy.Serpent()], 'fight'),
            Behavior(
                RectVector(23, 1, 24, 1),
                Vector(1, 0),
                self._start_fight,
                [Enemy.Dragon()],
                'fight',
            ),
            Behavior(
                RectVector(29, 4, 30, 4),
                Vector(1, 0),
                self._start_fight,
                [Enemy.Werewolf()],
                'fight',
            ),
            Behavior(
                RectVector(72, 16, 77, 16),
                Vector(1, 1),
                self._display_message,
                [
                    """It's a dangerous world. Take the bandages in the \
bottom left of my home. You'll need them.""", 0
                ],
                'pickup',
            ),
            Behavior(
                Vector(16, 13),
                Vector(0, 1),
                self._add_to_inventory,
                [Item.Key()],
                'pickup',
                True,
            ),
            Behavior(
                RectVector(23, 3, 24, 3),
                Vector(1, 0),
                self._unlock_door,
                [
                    Vector(23, 2),
                    Vector(1, 0), Item.Key(),
                    "You need a key to fight the final boss."
                ],
                'unlock',
            ),
            Behavior(
                RectVector(2, 13, 6, 13),
                Vector(0, 0),
                self._display_message,
                [
                    """There is some spare armor somewhere in the bottom of \
my house. Why don't you go get it.""", 0
                ],
                'message',
            ),
            Behavior(
                Vector(4, 16),
                Vector(0, 0),
                self._add_to_inventory,
                [Armor.Chestplate()],
                'pickup',
                True,
            )
        ]

    def _add_to_inventory(self, state: AbstractGameState,
                          *items: Item) -> None:
        state.player.inventory.extend(items)
        self._display_message(
            state, 'You picked up ' + ', '.join(map(str, items)) + '.', 4)

    def _start_fight(self, state: AbstractGameState, enemy: Enemy) -> None:
        if sum(1 for x in state.player.inventory
               if isinstance(x, Weapon)) == 0:
            state.pending_messages.append(
                "It isn't wise to fight without a weapon!")
            state.pending_message_timeouts.append(4)
            return
        state.gameplay_state = 'fight'
        state.target = enemy

    def _unlock_door(self, state: AbstractGameState, door: Vector, map: Vector,
                     key: Item, reject: str):
        if any(key == x for x in state.player.inventory):
            state.get_map(*map).set(door.x, door.y, ' ')
        else:
            self._display_message(state, reject)

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
