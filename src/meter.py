from typing import Any, Union

from .tracker import Tracker


class Meter:
    def __init__(self, tracker: Tracker):
        self.cursor = 0
        self.checkpoint = []
        self.tracker = tracker

    def append(self, value: Union[int, float]):
        self.tracker.append(value)

    def get(self, index: int) -> Any:
        # TODO: Support negative index
        if index < 0:
            raise IndexError(f'index {index} out of length {self.cursor}')

        # If index is less than cursor, return value in checkpoint
        if index < self.cursor:
            return self.checkpoint[index]
        # If index is greater than cursor, raise IndexError
        if index > self.cursor:
            raise IndexError(f'index {index} out of length {self.cursor}')
        # If index equals to cursor, return value in tracker
        return self.tracker.latest()

    def get_latest(self, complete: bool = False) -> Any:
        if complete:
            if self.cursor > 0:
                return self.checkpoint[-1]
            else:
                raise IndexError('no completed checkpoint')
        return self.tracker.latest()

    def step(self):
        self.cursor += 1
        self.checkpoint.append(self.tracker.latest())
        self.tracker.reset()

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def __len__(self) -> int:
        return self.cursor
