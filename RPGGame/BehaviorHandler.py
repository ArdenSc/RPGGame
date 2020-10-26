from functools import partial
from typing import Callable, List

from typing_extensions import TypedDict

from RPGGame.abstract.AbstractBehaviorHandler import AbstractBehaviorHandler
from RPGGame.abstract.AbstractEnemy import AbstractEnemy
from RPGGame.GameState import GameState
from RPGGame.Item import Item
from RPGGame.Vector import Vector


class Behavior(TypedDict):
    trigger_pos: Vector
    trigger_map: Vector
    handler: Callable[[GameState], None]
    one_time: bool


class BehaviorHandler(AbstractBehaviorHandler):
    def __init__(self):
        self._behaviors: List[Behavior] = [{
            "trigger_pos":
            Vector(20, 5),
            "trigger_map":
            Vector(0, 0),
            "handler":
            partial(self._add_to_inventory, item=Item("Sword")),
            "one_time":
            True
        }]

    def _add_to_inventory(self, state: GameState, item: Item) -> None:
        state.inventory.append(item)

    def _start_fight(self, state: GameState, enemy: AbstractEnemy) -> None:
        state.gameplay_state = "fight"
        state.target = enemy

    def on_move_callback(self, state: GameState) -> None:
        for behavior in self._behaviors:
            if behavior["trigger_pos"] == state.pos and behavior[
                    "trigger_map"] == state.map_pos:
                behavior["handler"](state)
