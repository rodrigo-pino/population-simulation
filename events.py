from typing import Callable
from sortedcontainers import SortedSet


class Event:
    def __init__(self, time: int) -> None:
        self._time = time

    @property
    def time(self) -> int:
        return self.time


class EventList:
    def __init__(self) -> None:
        sort_events: Callable[[Event], int] = lambda x: x.time
        self._events: SortedSet = SortedSet(key=sort_events)

    def add(self, event: Event) -> None:
        self._events.add(event)

    def next(self) -> Event:
        next_event: Event = self._events.pop(0)
        return next_event
