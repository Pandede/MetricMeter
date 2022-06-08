from math import sqrt
from typing import List

import pytest
from src.tracker import StdTracker

from .conftest import SEQUENCE


@pytest.fixture(autouse=True)
def tracker():
    return StdTracker()


def std(sequence):
    n = len(sequence)
    if n == 1:
        return 0.0
    mean = sum(sequence) / n
    return sqrt(sum((i - mean)**2 for i in sequence) / n)


class TestStdTracker:
    @staticmethod
    def __rough_equal(a, b, eps=1e-5):
        return abs(a - b) <= eps

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_append(self, tracker: StdTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert len(tracker) == i
            assert self.__rough_equal(tracker.latest(), std(sequence[:i]))

    def test_reset(self, tracker: StdTracker):
        # Insert dummy value and assert it's appended
        for _ in range(5):
            tracker.append(1)
        assert tracker.latest() == 0.
        assert len(tracker) == 5

        tracker.reset()
        assert tracker.latest() == 0.
        assert len(tracker) == 0

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_latest(self, tracker: StdTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert self.__rough_equal(tracker.latest(), std(sequence[:i]))
