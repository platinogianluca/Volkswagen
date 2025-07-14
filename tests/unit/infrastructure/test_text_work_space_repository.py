import pytest
from src.infrastructure.text_work_space_repository import TextWorkSpaceRepository
from src.domain.workspace.entity import WorkSpace


class TestTextWorkSpaceRepository:

    @pytest.mark.parametrize(
        "input_text,expected_max_x,expected_max_y",
        [
            pytest.param(
                "5 5\n1 2 N\nLMLMLMLMM",
                5, 5,
                id="standard_5x5_workspace_with_robot_data"
            ),
            pytest.param(
                "10 15\n0 0 N\nM\n5 5 E\nL",
                10, 15,
                id="rectangular_10x15_workspace_with_multiple_robots"
            ),
        ]
    )
    def test_get_workspace_parses_dimensions_correctly(
        self, input_text, expected_max_x, expected_max_y
    ):
        # Arrange
        repository = TextWorkSpaceRepository(input_text=input_text)

        # Act
        workspace = repository.get_workspace()

        # Assert
        assert isinstance(workspace, WorkSpace)
        assert workspace.max_x == expected_max_x
        assert workspace.max_y == expected_max_y

    @pytest.mark.parametrize(
        "invalid_dimensions",
        [
            pytest.param(
                "5\n1 2 N\nM",
                id="single_dimension_missing_y_coordinate"
            ),
            pytest.param(
                "5 5 5\n1 2 N\nM",
                id="three_dimensions_too_many_coordinates"
            ),
            pytest.param(
                "\n1 2 N\nM",
                id="empty_first_line_no_dimensions"
            ),
            pytest.param(
                "   \n1 2 N\nM",
                id="whitespace_only_first_line"
            ),
        ]
    )
    def test_get_workspace_raises_error_for_invalid_dimensions(
        self, invalid_dimensions
    ):
        # Arrange
        repository = TextWorkSpaceRepository(input_text=invalid_dimensions)

        # Act & Assert
        with pytest.raises(ValueError):
            repository.get_workspace()

    @pytest.mark.parametrize(
        "invalid_coordinates",
        [
            pytest.param(
                "abc def\n1 2 N\nM",
                id="non_numeric_coordinates_letters"
            ),
            pytest.param(
                "5.5 10.5\n1 2 N\nM",
                id="float_coordinates_not_integers"
            ),
            pytest.param(
                "5 abc\n1 2 N\nM",
                id="mixed_valid_and_invalid_coordinates"
            ),
        ]
    )
    def test_get_workspace_raises_error_for_non_integer_coordinates(
        self, invalid_coordinates
    ):
        # Arrange
        repository = TextWorkSpaceRepository(input_text=invalid_coordinates)

        # Act & Assert
        with pytest.raises(ValueError):
            repository.get_workspace()