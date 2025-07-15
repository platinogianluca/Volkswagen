from src.infrastructure.text_work_space_repository import TextWorkSpaceRepository
from src.application.services.work_space import WorkSpaceService
from src.application.services.robot_service import RobotService
from src.infrastructure.text_robot_repository import TextRobotRepository
from src.infrastructure.file_input_reader import FileInputReader


def main():
    file_input_adapter = FileInputReader()
    input_text = file_input_adapter.get_input("input.txt")

    workspace_service = WorkSpaceService(
        workspace_repository=TextWorkSpaceRepository(input_text=input_text)
    )
    robot_service = RobotService(
        robot_repository=TextRobotRepository(input_text=input_text),
        workspace_service=workspace_service
    )

    robot_position_orientation = robot_service.process_instructions()
    print(robot_position_orientation)


if __name__ == "__main__":
    main()
