from abc import ABC, abstractmethod
from src.domain.workspace.entity import WorkSpace


class WorkSpaceRepository(ABC):
 
     @abstractmethod
     def get_workspace(self) -> WorkSpace:
         raise NotImplementedError