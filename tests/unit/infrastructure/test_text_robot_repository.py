import pytest
from src.infrastructure.text_robot_repository import TextRobotRepository

class TestTextRobotRepository:

    @pytest.mark.parametrize(
        "input_text,expected_positions,expected_orientations,expected_instructions",
        [
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM",
                [(1, 2)],
                ["N"],
                ["LMLMLMLMM"],
                id="single_robot_with_complex_instructions",
            ),
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM",
                [(1, 2), (3, 3)],
                ["N", "E"],
                ["LMLMLMLMM", "MMRMMRMRRM"],
                id="two_robots_with_different_configurations",
            ),
            pytest.param(
                "10 10\n0 0 N\nM\n5 5 S\nL\n2 3 W\nR",
                [(0, 0), (5, 5), (2, 3)],
                ["N", "S", "W"],
                ["M", "L", "R"],
                id="three_robots_with_simple_instructions",
            ),
        ],
    )
    def test_parse_input_text_creates_correct_data_structures(
        self,
        input_text,
        expected_positions,
        expected_orientations,
        expected_instructions,
    ):
        # Act
        repository = TextRobotRepository(input_text=input_text)

        # Assert
        positions = repository.get_robot_position_list()
        orientations = repository.get_robot_orientation_list()
        instructions = repository.get_robot_instruction_list()

        # Verify positions
        assert len(positions) == len(expected_positions)
        for i, (expected_x, expected_y) in enumerate(expected_positions):
            assert positions[i].x == expected_x
            assert positions[i].y == expected_y

        # Verify orientations
        assert len(orientations) == len(expected_orientations)
        for i, expected_orientation in enumerate(expected_orientations):
            assert orientations[i].current_orientation == expected_orientation

        # Verify instructions
        assert instructions == expected_instructions

    @pytest.mark.parametrize(
        "invalid_input",
        [
            pytest.param(
                "5 5",
                id="only_workspace_dimensions_no_robot_data",
            ),
            pytest.param(
                "5 5\n1 2 N",
                id="workspace_and_position_but_no_instructions",
            ),
            pytest.param(
                "",
                id="empty_input_string",
            ),
            pytest.param(
                "\n\n",
                id="only_newlines_no_content",
            ),
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM\n3 3 E",
                id="missing_instruction_for_second_robot",
            ),
        ],
    )
    def test_parse_input_text_raises_error_for_invalid_input(
        self, invalid_input
    ):
        # Act & Assert
        with pytest.raises(ValueError):
            TextRobotRepository(input_text=invalid_input)