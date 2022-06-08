from typing import List

import pytest
from src.tracker import SumTracker

from .conftest import SEQUENCE


@pytest.fixture(autouse=True)
def tracker():
    return SumTracker()


class TestSumTracker:
    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_append(self, tracker: SumTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert tracker.latest() == sum(sequence[:i])

    def test_reset(self, tracker: SumTracker):
        # Insert dummy value and assert it's appended
        for _ in range(5):
            tracker.append(1)
        assert tracker.latest() == 5.
        assert len(tracker) == 5

        tracker.reset()
        assert tracker.latest() == 0.
        assert len(tracker) == 0

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_latest(self, tracker: SumTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert tracker.latest() == sum(sequence[:i])
