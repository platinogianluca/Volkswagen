from src.domain.robot.value_objects import Position

class WorkSpace:
    def __init__(self, max_x: int, max_y: int):
        if max_x <= 0 or max_y <= 0:
            raise ValueError(
                f"Workspace dimensions must be non-negative, "
                f"got max_x={max_x}, max_y={max_y}"
            )
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = 0
        self.min_y = 0
        
    def is_position_valid(self, position: Position) -> bool:
        return self.min_x <= position.x <= self.max_x and \
               self.min_y <= position.y <= self.max_y