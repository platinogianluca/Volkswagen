from unittest.mock import Mock
from src.application.services.work_space import WorkSpaceService
from src.application.repository.work_space_repository import WorkSpaceRepository
from src.domain.workspace.entity import WorkSpace


class TestWorkSpaceService:

    def test_get_workspace_returns_workspace_from_repository(self):
        # Arrange
        expected_workspace = Mock(spec=WorkSpace)
        workspace_repository = Mock(spec=WorkSpaceRepository)
        workspace_repository.get_workspace.return_value = expected_workspace

        # Act
        service = WorkSpaceService(workspace_repository=workspace_repository)
        result = service.get_workspace()

        # Assert
        assert result == expected_workspace
        workspace_repository.get_workspace.assert_called_once()
