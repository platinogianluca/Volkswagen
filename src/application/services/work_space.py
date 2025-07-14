from src.application.repository.work_space_repository import WorkSpaceRepository
from src.domain.workspace.entity import WorkSpace


class WorkSpaceService:
    def __init__(self, workspace_repository: WorkSpaceRepository):
        self.workspace_repository = workspace_repository

    def get_workspace(self) -> WorkSpace:
        return self.workspace_repository.get_workspace()