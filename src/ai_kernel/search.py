from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    @abstractmethod
    def propose(self, population, count: int):
        raise NotImplementedError
