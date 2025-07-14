from src.infrastructure.text_work_space_repository import TextWorkSpaceRepository
from src.application.services.work_space import WorkSpaceService
from src.application.services.robot_service import RobotService
from src.infrastructure.text_robot_repository import TextRobotRepository
from src.infrastructure.file_input_reader import FileInputReader


def main():
    file_input_reader = FileInputReader()
    input_text = file_input_reader.get_input("input.txt")

    robot_service = RobotService(
        robot_repository=TextRobotRepository(input_text=input_text)
    )
    workspace_service = WorkSpaceService(
        workspace_repository=TextWorkSpaceRepository(input_text=input_text)
    )

    workspace = workspace_service.get_workspace()
    output_text = robot_service.process_instructions(workspace)
    print(output_text)


if __name__ == "__main__":
    main()
