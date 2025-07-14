from src.domain.workspace.entity import WorkSpace
import pytest
from unittest.mock import Mock

from src.domain.robot.entity import Robot
from src.domain.robot.value_objects import Position, Orientation


class TestRobot:

    def setup_method(self):
        self.initial_position = Mock(spec=Position)
        self.initial_orientation = Mock(spec=Orientation)
        self.workspace = Mock(spec=WorkSpace)
        self.robot = Robot(self.initial_position, self.initial_orientation)

    def test_robot_initialization(self):
        # Assert
        assert self.robot.position == self.initial_position
        assert self.robot.orientation == self.initial_orientation

    def test_turn_left_calls_orientation_turn_left(self):
        # Arrange
        new_orientation = Mock(spec=Orientation)
        self.initial_orientation.turn_left.return_value = new_orientation

        # Act
        self.robot._turn_left()

        # Assert
        self.initial_orientation.turn_left.assert_called_once()
        assert self.robot.orientation == new_orientation

    def test_turn_right_calls_orientation_turn_right(self):
        # Arrange
        new_orientation = Mock(spec=Orientation)
        self.initial_orientation.turn_right.return_value = new_orientation

        # Act
        self.robot._turn_right()

        # Assert
        self.initial_orientation.turn_right.assert_called_once()
        assert self.robot.orientation == new_orientation

    def test_move_forward_valid_position(self):
        # Arrange
        next_position = Mock(spec=Position)
        self.initial_position.move.return_value = next_position
        self.workspace.is_position_valid.return_value = True
        # Act
        self.robot._move_forward(self.workspace)

        # Assert
        self.initial_position.move.assert_called_once_with(self.initial_orientation)
        assert self.robot.position == next_position

    def test_move_forward_invalid_position_raises_value_error(self):
        # Arrange
        next_position = Mock(spec=Position)
        self.initial_position.move.return_value = next_position
        self.workspace.is_position_valid.return_value = False

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.robot._move_forward(self.workspace)

        assert (
            str(exc_info.value)
            == f"Position {next_position} is out of workspace bounds"
        )

    @pytest.mark.parametrize(
        "command,expected_method",
        [
            pytest.param(
                "L", "_turn_left", id="L_command_should_execute_turn_left_method"
            ),
            pytest.param(
                "R", "_turn_right", id="R_command_should_execute_turn_right_method"
            ),
            pytest.param(
                "M", "_move_forward", id="M_command_should_execute_move_forward_method"
            ),
        ],
    )
    def test_execute_instructions_single_command(self, command, expected_method):
        # Arrange
        method_mock = Mock()
        setattr(self.robot, expected_method, method_mock)
        # Act
        self.robot.execute_instructions(command, self.workspace)
        # Assert
        method_mock.assert_called_once()

    @pytest.mark.parametrize(
        "commands,expected_methods",
        [
            pytest.param(
                "LR",
                ["_turn_left", "_turn_right"],
                id="LR_commands_should_execute_left_then_right_turns",
            ),
            pytest.param(
                "LRM",
                ["_turn_left", "_turn_right", "_move_forward"],
                id="LRM_commands_should_execute_left_right_move_sequence",
            ),
            pytest.param(
                "MMLL",
                ["_move_forward", "_move_forward", "_turn_left", "_turn_left"],
                id="MMLL_commands_should_execute_two_moves_then_two_left_turns",
            ),
            pytest.param(
                "RML",
                ["_turn_right", "_move_forward", "_turn_left"],
                id="RML_commands_should_execute_right_move_left_sequence",
            ),
        ],
    )
    def test_execute_instructions_multiple_commands(self, commands, expected_methods):
        # Arrange - Mock all unique methods
        method_mocks = {}
        for method_name in set(expected_methods):
            method_mocks[method_name] = Mock()
            setattr(self.robot, method_name, method_mocks[method_name])

        # Act
        self.robot.execute_instructions(commands, self.workspace)

        # Assert - Check each method was called the correct number of times
        for method_name, mock in method_mocks.items():
            expected_count = expected_methods.count(method_name)
            assert mock.call_count == expected_count

    @pytest.mark.parametrize(
        "invalid_instructions",
        [
            pytest.param("XYZ", id="invalid_letters_XYZ_should_raise_error"),
            pytest.param("123", id="numeric_characters_123_should_raise_error"),
            pytest.param("ABCD", id="invalid_letters_ABCD_should_raise_error"),
            pytest.param(" ", id="whitespace_character_should_raise_error"),
        ],
    )
    def test_execute_instructions_invalid_commands(self, invalid_instructions: str):
        # Arrange
        self.robot._turn_left = Mock()
        self.robot._turn_right = Mock()
        self.robot._move_forward = Mock()
        # Act
        with pytest.raises(ValueError):
            self.robot.execute_instructions(invalid_instructions, self.workspace)
        # Assert
        self.robot._turn_left.assert_not_called()
        self.robot._turn_right.assert_not_called()
        self.robot._move_forward.assert_not_called()

    def test_get_state_returns_current_position_and_orientation(self):
        # Act
        position, orientation = self.robot.get_state()

        # Assert
        assert position == self.initial_position
        assert orientation == self.initial_orientation
