from src.domain.workspace.entity import WorkSpace
from src.application.repository.work_space_repository import WorkSpaceRepository


class TextWorkSpaceRepository(WorkSpaceRepository):
    def __init__(self, input_text: str):
        self.input_text = input_text

    def get_workspace(self) -> WorkSpace:
        lines = self.input_text.strip().split("\n")

        workspace_line = lines[0].split()
        if len(workspace_line) != 2:
            raise ValueError("Workspace dimensions must be specified as 'X Y'")
        workspace_x, workspace_y = int(workspace_line[0]), int(workspace_line[1])
        return WorkSpace(max_x=workspace_x, max_y=workspace_y)