from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def results(self):
        pass
    @abstractmethod
    def entries(self):
        pass
    @abstractmethod
    def exits(self):
        pass