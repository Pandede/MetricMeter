from typing import List

import pytest
from src.meter import Meter
from src.tracker import DummyTracker

from .conftest import SEQUENCE


@pytest.fixture
def meter():
    return Meter(DummyTracker())


class TestMeter:
    @pytest.mark.parametrize('sequence', SEQUENCE)
    def test_append(self, meter: Meter, sequence: List[List[float]]):
        last_values = []
        for i, arr in enumerate(sequence):
            for n in arr:
                meter.append(n)
                assert meter.cursor == i
                assert meter.get_latest() == n
            last_values.append(n)
            meter.step()
            assert meter.get_latest() is None
        assert last_values == meter.checkpoint

    class TestGet:
        @pytest.mark.parametrize('sequence', SEQUENCE)
        def test_index_less_than(self, meter: Meter, sequence: List[List[float]]):
            last_values = []
            for arr in sequence:
                for n in arr:
                    meter.append(n)
                last_values.append(n)
                meter.step()

            for i, arr in enumerate(sequence):
                assert meter.get(i) == arr[-1]
                assert meter[i] == arr[-1]

        @pytest.mark.parametrize('sequence', SEQUENCE)
        def test_index_equals(self, meter: Meter, sequence: List[List[float]]):
            for i, arr in enumerate(sequence):
                for n in arr:
                    meter.append(n)
                    assert meter.get(i) == n
                    assert meter[i] == n
                meter.step()

        def test_index_greater_than(self, meter: Meter):
            with pytest.raises(IndexError):
                meter.get(1)
                meter[1]

            meter.append(0.0)
            meter.step()

            with pytest.raises(IndexError):
                meter.get(2)
                meter[2]

        def test_negative_index(self, meter: Meter):
            with pytest.raises(IndexError):
                meter.get(-1)
                meter[-1]

    class TestGetLatest:
        @pytest.mark.parametrize('sequence', SEQUENCE)
        def test_no_step(self, meter: Meter, sequence: List[List[float]]):
            assert meter.get_latest() is None

            for arr in sequence:
                for n in arr:
                    meter.append(n)
                    assert meter.get_latest() == n

        def test_after_step(self, meter: Meter):
            meter.append(0.0)
            meter.step()
            assert meter.get_latest() is None

        @pytest.mark.parametrize('sequence', SEQUENCE)
        def test_complete_normal(self, meter: Meter, sequence: List[List[float]]):
            for arr in sequence:
                for n in arr:
                    meter.append(n)
                meter.step()
                assert meter.get_latest(complete=True) == n

        def test_complete_but_empty_checkpoint(self, meter: Meter):
            with pytest.raises(IndexError):
                meter.get_latest(complete=True)

            with pytest.raises(IndexError):
                meter.append(0.0)
                meter.get_latest(complete=True)

            meter.step()
            assert meter.get_latest(complete=True) == 0.0

    def test_len(self, meter: Meter):
        assert len(meter) == 0
        meter.step()
        assert len(meter) == 1
