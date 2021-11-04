from typing import Callable, List, Tuple
from sortedcontainers import SortedSet


class Event:
    def __init__(self, time: int, priority: int = 0) -> None:
        self._time = time
        self._priority = priority

    @property
    def time(self) -> int:
        return self._time

    @property
    def priority(self) -> int:
        return self._priority


class EventList:
    def __init__(self, initial_events: List[Event]) -> None:
        sort_events: Callable[[Event], Tuple[int, int]] = lambda x: (
            x.time,
            x.priority,
        )
        self._events: SortedSet = SortedSet(initial_events, key=sort_events)
        self._current_time = 0

    def add(self, event: Event) -> None:
        self._events.add(event)

    def next(self) -> Event:
        next_event: Event = self._events.pop(0)
        return next_event

    @property
    def current_time(self) -> int:
        return self.current_time


# e1 = Event(0, 1)
# e2 = Event(1, 1)
# e3 = Event(1, 2)

# el = EventList([e1, e2, e3])

# print(el.next().priority)
# print(el.next().priority)
# print(el.next().priority)
