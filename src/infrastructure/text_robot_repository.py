from src.application.repository.robot_repository import RobotRepository
from src.domain.robot.value_objects import Position, Orientation
from src.domain.workspace.entity import WorkSpace


class TextRobotRepository(RobotRepository):
    def __init__(self, input_text: str):
        (
            self.position_list,
            self.orientation_list,
            self.instructions_list,
        ) = self._parse_input_text(input_text)

    def _parse_input_text(
        self, input_text: str
    ) -> tuple[WorkSpace, list[Position], list[Orientation], list[str]]:
        try:
            lines = input_text.strip().split("\n")
            if len(lines) < 3:
                raise ValueError(
                    "Input must contain at least 3 lines: "
                    "workspace dimensions and at least one robot configuration"
                )
            position_list = []
            orientation_list = []
            instruction_list = []

            for i in range(1, len(lines), 2):
                position_line = lines[i].split()
                position_x = int(position_line[0])
                position_y = int(position_line[1])
                orientation = position_line[2]
                position_list.append(Position(position_x, position_y))
                orientation_list.append(Orientation(orientation))
                instruction_list.append(lines[i + 1])

            return position_list, orientation_list, instruction_list
        except IndexError as e:
            raise ValueError(
                "Invalid input format. Ensure the input is correctly formatted."
            ) from e

    def get_robot_position_list(self) -> list[Position]:
        return self.position_list

    def get_robot_orientation_list(self) -> list[Orientation]:
        return self.orientation_list

    def get_robot_instruction_list(self) -> list[str]:
        return self.instructions_list
