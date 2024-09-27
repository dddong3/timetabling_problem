from abc import ABC, abstractmethod

class FitnessBase(ABC):
    name = None
    description = None
    weight = None
    @abstractmethod
    def evaluate(self, individual):
        pass