import pytest
from unittest.mock import Mock

from src.domain.workspace.entity import WorkSpace
from src.domain.robot.value_objects import Position


class TestWorkspace:

    def test_workspace_initialization(self):
        # Act
        max_x = 5
        max_y = 5
        workspace = WorkSpace(max_x, max_y)
        # Assert
        assert workspace.max_x ==max_x
        assert workspace.max_y ==max_y
        assert workspace.min_x == 0
        assert workspace.min_y == 0

    @pytest.mark.parametrize(
        "max_x,max_y",
        [
            pytest.param(1, 1, id="minimum_valid_dimensions"),
            pytest.param(10, 5, id="rectangular_workspace"),
            pytest.param(100, 200, id="large_workspace_dimensions"),
        ],
    )
    def test_workspace_initialization_valid_dimensions(self, max_x, max_y):
        # Act
        workspace = WorkSpace(max_x, max_y)
        # Assert
        assert workspace.max_x == max_x
        assert workspace.max_y == max_y
        assert workspace.min_x == 0
        assert workspace.min_y == 0

    @pytest.mark.parametrize(
        "max_x,max_y",
        [
            pytest.param(0, 0, id="zero_dimensions"),
            pytest.param(0, 1, id="zero_width"),
            pytest.param(1, 0, id="zero_height"),
            pytest.param(-1, 0, id="negative_width"),
            pytest.param(0, -1, id="negative_height"),
            pytest.param(-1, -1, id="negative_dimensions"),
            pytest.param(-5, 10, id="negative_width_positive_height"),
            pytest.param(10, -5, id="positive_width_negative_height"),
        ],
    )
    def test_workspace_initialization_invalid_dimensions_raises_error(self, max_x, max_y):
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            WorkSpace(max_x, max_y)

        expected_message = (
            f"Workspace dimensions must be non-negative, "
            f"got max_x={max_x}, max_y={max_y}"
        )
        assert str(exc_info.value) == expected_message

    @pytest.mark.parametrize(
        "x,y,expected",
        [
            pytest.param(0, 0, True, id="bottom_left_corner"),
            pytest.param(5, 5, True, id="top_right_corner"),
            pytest.param(2, 3, True, id="inside_workspace"),
            pytest.param(0, 5, True, id="left_edge"),
            pytest.param(5, 0, True, id="bottom_edge"),
            pytest.param(3, 0, True, id="bottom_middle"),
            pytest.param(0, 3, True, id="left_middle"),
            pytest.param(-1, 0, False, id="left_of_workspace"),
            pytest.param(0, -1, False, id="below_workspace"),
            pytest.param(6, 0, False, id="right_of_workspace"),
            pytest.param(0, 6, False, id="above_workspace"),
            pytest.param(-1, -1, False, id="bottom_left_outside"),
            pytest.param(6, 6, False, id="top_right_outside"),
            pytest.param(10, 3, False, id="far_right"),
            pytest.param(3, 10, False, id="far_above"),
        ],
    )
    def test_is_position_valid(self, x, y, expected):
        # Arrange
        max_x = 5
        max_y = 5
        workspace = WorkSpace(max_x, max_y)
        position = Mock(spec=Position)
        position.x = x
        position.y = y

        # Act
        result = workspace.is_position_valid(position)

        # Assert
        assert result == expected