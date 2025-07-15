from unittest.mock import Mock, patch, mock_open
from main import main
import pytest


class TestMainIntegration:

    @pytest.mark.parametrize(
        "input_text, expected_output",
        [
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM", "1 3 N", id="single_robot_navigation_1"
            ),
            pytest.param(
                "5 5\n3 3 E\nMMRMMRMRRM", "5 1 E", id="single_robot_navigation_2"
            ),
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM",
                "1 3 N\n5 1 E",
                id="multiple_robots_navigation",
            ),
        ],
    )
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_main_integration_with_sample_input(
        self, mock_print: Mock, mock_file: Mock, input_text: str, expected_output: str
    ):
        # Arrange
        mock_file.return_value.read.return_value = input_text
        # Act
        main()
        # Assert
        mock_file.assert_called_once_with("input.txt", "r")
        mock_print.assert_called_once_with(expected_output)

    @pytest.mark.parametrize(
        "input_text",
        [
            pytest.param("-1 0\n1 2 N\nR", id="negative_grid_width"),
            pytest.param("0 -1\n1 2 N\nR", id="negative_grid_height"),
            pytest.param("0 0\n1 2 N\nR", id="zero_grid_dimensions"),
            pytest.param("1 0\n1 2 N\nR", id="zero_grid_width"),
            pytest.param("0 1\n1 2 N\nR", id="zero_grid_height"),
            pytest.param("1 1\n2 2 E\nR", id="robot_outside_grid_boundaries"),
            pytest.param("1 1\n1 1 N\nM", id="robot_moving_outside_grid_boundaries"),
            pytest.param("1 1\n0 0 X\nM", id="invalid_robot_orientation"),
            pytest.param("1 1\n0 0 N\nX", id="invalid_robot_instruction"),
            pytest.param("5", id="missing_grid_height"),
            pytest.param("5 5", id="missing_robot_data"),
            pytest.param("5 5\n1 2 N", id="missing_robot_instructions"),
            pytest.param("5 5\n1 2 N\n", id="empty_robot_instructions"),
            pytest.param("5 5\n1 2 N\nLMLMLMLMM\n0 0", id="empty_last_robot_instructions"),
        ],
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_main_integration_with_incorrect_input(
        self, mock_file: Mock, input_text: str
    ):
        # Arrange
        mock_file.return_value.read.return_value = input_text
        # Act
        with pytest.raises(ValueError):
            main()
        # Assert
        mock_file.assert_called_once_with("input.txt", "r")
