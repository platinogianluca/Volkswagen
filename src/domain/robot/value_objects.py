from dataclasses import dataclass
from typing_extensions import Literal


@dataclass(frozen=True)
class Orientation:
    current_orientation: Literal["N", "E", "S", "W"]

    _TURN_LEFT_MAP = {"N": "W", "W": "S", "S": "E", "E": "N"}

    _TURN_RIGHT_MAP = {"N": "E", "E": "S", "S": "W", "W": "N"}

    def __post_init__(self):
        if self.current_orientation not in self._TURN_LEFT_MAP:
            raise ValueError(
                f"Invalid orientation: {self.current_orientation}. "
                f"Must be one of {list(self._TURN_LEFT_MAP.keys())}"
            )


    def turn_left(self) -> "Orientation":
        new_orientation = self._TURN_LEFT_MAP[self.current_orientation]
        return Orientation(new_orientation)

    def turn_right(self) -> "Orientation":
        new_value = self._TURN_RIGHT_MAP[self.current_orientation]
        return Orientation(new_value)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def move(self, orientation: Orientation) -> "Position":
        if orientation.current_orientation == "N":
            return Position(self.x, self.y + 1)
        if orientation.current_orientation == "E":
            return Position(self.x + 1, self.y)
        if orientation.current_orientation == "S":
            return Position(self.x, self.y - 1)
        if orientation.current_orientation == "W":
            return Position(self.x - 1, self.y)