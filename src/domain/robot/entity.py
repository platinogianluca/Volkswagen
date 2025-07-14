from src.domain.workspace.entity import WorkSpace
from src.domain.robot.value_objects import Position, Orientation


class Robot:
    def __init__(self, position: Position, orientation: Orientation):
        self.position = position
        self.orientation = orientation

    def _turn_left(self):
        self.orientation = self.orientation.turn_left()

    def _turn_right(self):
        self.orientation = self.orientation.turn_right()

    def _move_forward(self, workspace: WorkSpace):
        next_position = self.position.move(self.orientation)
        if not workspace.is_position_valid(next_position):
            raise ValueError(
                f"Position {next_position} is out of workspace bounds"
            )
        self.position = next_position

    def execute_instructions(self, instructions: str, workspace: WorkSpace):
        for command in instructions:
            if command == "L":
                self._turn_left()
            elif command == "R":
                self._turn_right()
            elif command == "M":
                self._move_forward(workspace)
            else:
                raise ValueError(f"Invalid instruction: {command}")

    def get_state(self) -> tuple[Position, Orientation]:
        return self.position, self.orientation
