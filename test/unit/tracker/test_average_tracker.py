from typing import List

import pytest
from src.tracker import AverageTracker

from .conftest import SEQUENCE


@pytest.fixture(autouse=True)
def tracker():
    return AverageTracker()


class TestAverageTracker:
    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_append(self, tracker: AverageTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert len(tracker) == i
            assert tracker.latest() == sum(sequence[:i]) / i

    def test_reset(self, tracker: AverageTracker):
        # Insert dummy value and assert it's appended
        for _ in range(5):
            tracker.append(1)
        assert tracker.latest() == 1.
        assert len(tracker) == 5

        tracker.reset()
        assert tracker.latest() == 0.
        assert len(tracker) == 0

    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_latest(self, tracker: AverageTracker, sequence: List[float]):
        for i, n in enumerate(sequence, 1):
            tracker.append(n)
            assert tracker.latest() == sum(sequence[:i]) / i
