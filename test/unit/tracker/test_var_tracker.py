from typing import List

import pytest
from src.tracker import VarTracker

from .conftest import SEQUENCE


@pytest.fixture(autouse=True)
def tracker():
    return VarTracker()


def variance(sequence):
    n = len(sequence)
    if n == 1:
        return 0.0
    mean = sum(sequence) / n
    return sum((i - mean)**2 for i in sequence) / n


class TestVarianceTracker:
    @staticmethod
    def __rough_equal(a, b, eps=1e-5):
        return abs(a - b) <= eps

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_append(self, tracker: VarTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert len(tracker) == i
            assert self.__rough_equal(tracker.latest(), variance(sequence[:i]))

    def test_reset(self, tracker: VarTracker):
        # Insert dummy value and assert it's appended
        for _ in range(5):
            tracker.append(1)
        assert tracker.latest() == 0.
        assert len(tracker) == 5

        tracker.reset()
        assert tracker.latest() == 0.
        assert len(tracker) == 0

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_latest(self, tracker: VarTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert self.__rough_equal(tracker.latest(), variance(sequence[:i]))
