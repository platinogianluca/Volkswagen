from src.domain.workspace.entity import WorkSpace
import pytest
from unittest.mock import Mock, patch
from src.application.services.robot_service import RobotService
from src.application.repository.robot_repository import RobotRepository
from src.domain.robot.value_objects import Position, Orientation


class TestRobotInstructionService:

    @pytest.mark.parametrize(
        "positions_data,orientations_data,expected_output",
        [
            pytest.param([(7, 9)], ["NE"], "7 9 NE", id="single_robot"),
            pytest.param([(1, 2), (3, 4)], ["N", "E"], "1 2 N\n3 4 E", id="two_robots"),
            pytest.param(
                [(0, 1), (2, 3), (5, 6)],
                ["W", "S", "E"],
                "0 1 W\n2 3 S\n5 6 E",
                id="three_robots",
            ),
        ],
    )
    def test_parse_robot_position_orientation_handles_multiple_elements(
        self, positions_data, orientations_data, expected_output
    ):
        # Arrange
        position_list = []
        orientation_list = []

        for i in range(len(positions_data)):
            position = Mock(spec=Position)
            position.x = positions_data[i][0]
            position.y = positions_data[i][1]
            position_list.append(position)

            orientation = Mock(spec=Orientation)
            orientation.current_orientation = orientations_data[i]
            orientation_list.append(orientation)

        # Act
        service = RobotService(robot_repository=Mock(spec=RobotRepository))
        result = service._parse_robot_position_orientation(
            position_list=position_list, orientation_list=orientation_list
        )

        # Assert
        assert result == expected_output

    @pytest.mark.parametrize(
        "expected_positions,expected_orientations",
        [
            pytest.param(
                [(1, 2)],
                ["N"],
                id="single_robot",
            ),
            pytest.param(
                [(1, 2), (3, 4)],
                ["N", "E"],
                id="two_robots",
            ),
            pytest.param(
                [(0, 1), (2, 3), (5, 6)],
                ["W", "S", "E"],
                id="three_robots",
            ),
        ],
    )
    @patch.object(RobotService, "_parse_robot_position_orientation")
    @patch("src.application.services.robot_service.Robot")
    def test_process_instructions_multiple_robots(
        self,
        mock_robot_class,
        mock_parse_method,
        expected_positions,
        expected_orientations,
    ):
        # Arrange
        workspace = Mock(spec=WorkSpace)
        workspace.is_position_valid.return_value = True

        num_robots = len(expected_positions)

        # Create dynamic mock lists based on number of robots
        instructions_list = [Mock(spec=str) for _ in range(num_robots)]
        positions_list = [Mock(spec=Position) for _ in range(num_robots)]
        orientations_list = [Mock(spec=Orientation) for _ in range(num_robots)]

        robot_repository = Mock(spec=RobotRepository)
        robot_repository.get_robot_instruction_list.return_value = instructions_list
        robot_repository.get_robot_position_list.return_value = positions_list
        robot_repository.get_robot_orientation_list.return_value = orientations_list

        # Mock robot behavior
        mock_robot = Mock()
        mock_robot_class.return_value = mock_robot

        # Create dynamic final positions and orientations
        final_states = []
        for i in range(num_robots):
            final_pos = Mock(spec=Position)
            final_pos.x = expected_positions[i][0]
            final_pos.y = expected_positions[i][1]

            final_ori = Mock(spec=Orientation)
            final_ori.current_orientation = expected_orientations[i]

            final_states.append((final_pos, final_ori))

        mock_robot.get_state.side_effect = final_states
        mock_result = Mock()
        mock_parse_method.return_value = mock_result

        # Act
        service = RobotService(robot_repository=robot_repository)
        result = service.process_instructions(workspace=workspace)

        # Assert
        assert result == mock_result
        assert mock_robot_class.call_count == num_robots
        assert mock_robot.execute_instructions.call_count == num_robots

    @patch("src.application.services.robot_service.Robot")
    def test_process_instructions_invalid_position_raises_error(self, mock_robot_class):
        # Arrange
        mock_robot = Mock()
        mock_robot_class.return_value = mock_robot
        workspace = Mock(spec=WorkSpace)
        workspace.is_position_valid.return_value = False

        robot_repository = Mock(spec=RobotRepository)
        robot_repository.get_robot_instruction_list.return_value = ["L"]
        robot_repository.get_robot_position_list.return_value = [Mock(spec=Position)]
        robot_repository.get_robot_orientation_list.return_value = [
            Mock(spec=Orientation)
        ]

        # Act & Assert
        with pytest.raises(ValueError):
            service = RobotService(robot_repository=robot_repository)
            service.process_instructions(workspace=workspace)
        mock_robot.execute_instructions.assert_not_called()
