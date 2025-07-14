import pytest
from src.domain.robot.value_objects import Position, Orientation


class TestOrientation:

    @pytest.mark.parametrize(
        "orientation,expected",
        [
            pytest.param("N", "N", id="north_orientation_should_remain_north"),
            pytest.param("E", "E", id="east_orientation_should_remain_east"),
            pytest.param("S", "S", id="south_orientation_should_remain_south"),
            pytest.param("W", "W", id="west_orientation_should_remain_west"),
        ],
    )
    def test_orientation_initialization_valid(self, orientation, expected):
        # Act
        result = Orientation(orientation)

        # Assert
        assert result.current_orientation == expected

    @pytest.mark.parametrize(
        "invalid_orientation",
        [
            pytest.param("X", id="invalid_letter_x_should_raise_error"),
            pytest.param("NE", id="multiple_letters_should_raise_error"),
            pytest.param("n", id="lowercase_letter_should_raise_error"),
            pytest.param("", id="empty_string_should_raise_error"),
            pytest.param("1", id="numeric_value_should_raise_error"),
            pytest.param(None, id="none_value_should_raise_error"),
        ],
    )
    def test_orientation_initialization_invalid_raises_error(self, invalid_orientation):
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Orientation(invalid_orientation)

        expected_message = (
            f"Invalid orientation: {invalid_orientation}. "
            f"Must be one of ['N', 'W', 'S', 'E']"
        )
        assert str(exc_info.value) == expected_message

    @pytest.mark.parametrize(
        "current,expected_left",
        [
            pytest.param("N", "W", id="from_north_turn_left_should_face_west"),
            pytest.param("W", "S", id="from_west_turn_left_should_face_south"),
            pytest.param("S", "E", id="from_south_turn_left_should_face_east"),
            pytest.param("E", "N", id="from_east_turn_left_should_face_north"),
        ],
    )
    def test_turn_left(self, current, expected_left):
        # Arrange
        orientation = Orientation(current)

        # Act
        result = orientation.turn_left()

        # Assert
        assert result.current_orientation == expected_left
        assert isinstance(result, Orientation)
        # Verify immutability - original should not change
        assert orientation.current_orientation == current

    @pytest.mark.parametrize(
        "current,expected_right",
        [
            pytest.param("N", "E", id="from_north_turn_right_should_face_east"),
            pytest.param("E", "S", id="from_east_turn_right_should_face_south"),
            pytest.param("S", "W", id="from_south_turn_right_should_face_west"),
            pytest.param("W", "N", id="from_west_turn_right_should_face_north"),
        ],
    )
    def test_turn_right(self, current, expected_right):
        # Arrange
        orientation = Orientation(current)

        # Act
        result = orientation.turn_right()

        # Assert
        assert result.current_orientation == expected_right
        assert isinstance(result, Orientation)
        # Verify immutability - original should not change
        assert orientation.current_orientation == current

    def test_orientation_is_frozen(self):
        # Arrange
        orientation = Orientation("N")

        # Act & Assert
        with pytest.raises(AttributeError):
            orientation.current_orientation = "E"

    def test_orientation_equality(self):
        # Arrange & Act
        orientation1 = Orientation("N")
        orientation2 = Orientation("N")
        orientation3 = Orientation("E")

        # Assert
        assert orientation1 == orientation2
        assert orientation1 != orientation3

class TestPosition:

    @pytest.mark.parametrize(
        "x,y",
        [
            pytest.param(0, 0, id="origin_position_should_be_created_successfully"),
            pytest.param(1, 1, id="positive_coordinates_should_be_created_successfully"),
        ],
    )
    def test_position_initialization(self, x, y):
        # Act
        position = Position(x, y)

        # Assert
        assert position.x == x
        assert position.y == y

    @pytest.mark.parametrize(
        "x,y,orientation,expected_x,expected_y",
        [
            pytest.param(1, 1, "N", 1, 2, id="move_north_from_1_1_should_reach_1_2"),
            pytest.param(1, 1, "E", 2, 1, id="move_east_from_1_1_should_reach_2_1"),
            pytest.param(1, 1, "S", 1, 0, id="move_south_from_1_1_should_reach_1_0"),
            pytest.param(1, 1, "W", 0, 1, id="move_west_from_1_1_should_reach_0_1"),
            pytest.param(0, 0, "N", 0, 1, id="move_north_from_origin_should_reach_0_1"),
            pytest.param(0, 0, "E", 1, 0, id="move_east_from_origin_should_reach_1_0"),
            pytest.param(5, 3, "S", 5, 2, id="move_south_from_5_3_should_reach_5_2"),
            pytest.param(5, 3, "W", 4, 3, id="move_west_from_5_3_should_reach_4_3"),
        ],
    )
    def test_move_in_all_directions(self, x, y, orientation, expected_x, expected_y):
        # Arrange
        position = Position(x, y)
        orientation_obj = Orientation(orientation)

        # Act
        new_position = position.move(orientation_obj)

        # Assert
        assert new_position.x == expected_x
        assert new_position.y == expected_y
        assert isinstance(new_position, Position)
        # Verify immutability - original should not change
        assert position.x == x
        assert position.y == y

    def test_position_is_frozen(self):
        # Arrange
        position = Position(1, 1)

        # Act & Assert
        with pytest.raises(AttributeError):
            position.x = 5

    def test_position_equality(self):
        # Arrange & Act
        position1 = Position(1, 1)
        position2 = Position(1, 1)
        position3 = Position(2, 1)

        # Assert
        assert position1 == position2
        assert position1 != position3
