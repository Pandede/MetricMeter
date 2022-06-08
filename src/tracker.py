
from abc import ABC, abstractmethod
from math import sqrt
from typing import Any, Union


class Tracker(ABC):
    def __init__(self):
        self.reset()
        self.count = 0

    @abstractmethod
    def append(self, value: Any):
        return NotImplemented

    @abstractmethod
    def clear(self):
        return NotImplemented

    def reset(self):
        self.clear()
        self.count = 0

    @abstractmethod
    def latest(self) -> Any:
        return NotImplemented

    def __len__(self):
        return self.count


class AverageTracker(Tracker):
    def __init__(self):
        super(AverageTracker, self).__init__()

    def append(self, value: Union[int, float]):
        self.mean = (self.mean * self.count + value) / (self.count + 1)
        self.count += 1

    def clear(self):
        self.mean = 0.

    def latest(self) -> float:
        return self.mean


class SumTracker(Tracker):
    def __init__(self):
        super(SumTracker, self).__init__()

    def append(self, value: Union[int, float]):
        self.sum += value
        self.count += 1

    def clear(self):
        self.sum = 0.

    def latest(self) -> float:
        return self.sum


class VarTracker(Tracker):
    def __init__(self):
        super(VarTracker, self).__init__()

    def append(self, value: Union[int, float]):
        self.count += 1
        new_mean = self.mean + (value - self.mean) / self.count
        self.var += (value - new_mean) * (value - self.mean)
        self.mean = new_mean

    def clear(self):
        self.mean = 0.
        self.var = 0.
    
    def latest(self) -> float:
        if self.count > 1:
            return self.var / self.count
        return 0.0

class StdTracker(VarTracker):
    def __init__(self):
        super(StdTracker, self).__init__()
    
    def latest(self) -> float:
        return sqrt(super().latest())
