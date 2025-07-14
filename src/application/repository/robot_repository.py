from abc import ABC, abstractmethod

from src.domain.robot.value_objects import Orientation, Position


class RobotRepository(ABC):

    @abstractmethod
    def get_robot_position_list(self) -> list[Position]:
        raise NotImplementedError

    @abstractmethod
    def get_robot_orientation_list(self) -> list[Orientation]:
        raise NotImplementedError

    @abstractmethod
    def get_robot_instruction_list(self) -> str:
        raise NotImplementedError