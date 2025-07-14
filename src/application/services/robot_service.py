from src.application.repository.robot_repository import RobotRepository
from src.application.services.work_space import WorkSpaceService
from src.domain.robot.entity import Robot
from src.domain.robot.value_objects import Position, Orientation
from src.domain.workspace.entity import WorkSpace


class RobotService:

    def __init__(self, robot_repository: RobotRepository):
        self.robot_repository = robot_repository

    def _parse_robot_position_orientation(
        self, position_list: list[Position], orientation_list: list[Orientation]
    ) -> str:
        result_position_orientation = []
        for i in range(len(position_list)):
            position = position_list[i]
            orientation = orientation_list[i]
            result_position_orientation.append(
                f"{position.x} {position.y} {orientation.current_orientation}"
            )
        return "\n".join(result_position_orientation)

    def process_instructions(self, workspace: WorkSpace) -> str:
        instruction_list = self.robot_repository.get_robot_instruction_list()
        initial_position_list = self.robot_repository.get_robot_position_list()
        initial_orientation_list = self.robot_repository.get_robot_orientation_list()

        final_position_list = []
        final_orientation_list = []
        for i in range(len(instruction_list)):
            if not workspace.is_position_valid(position=initial_position_list[i]):
                raise ValueError(
                    f"Initial position {initial_position_list} is out of workspace bounds"
                )

            robot = Robot(
                position=initial_position_list[i], orientation=initial_orientation_list[i]
            )
            robot.execute_instructions(
                instructions=instruction_list[i], workspace=workspace
            )
            final_position, final_orientation = robot.get_state()
            final_position_list.append(final_position)
            final_orientation_list.append(final_orientation)
        return self._parse_robot_position_orientation(
            position_list=final_position_list,
            orientation_list=final_orientation_list,
        )