from __future__ import annotations
from typing import Any, Callable, List, Tuple
from sortedcontainers import SortedSet


class Event:
    def __init__(
        self, action: Callable[..., str], time: int, priority: int = 0, *args: Any
    ) -> None:
        self._action = action
        self._time = time
        self._priority = priority
        self._args = args

    def execute(self):
        return self._action(*self._args)

    @property
    def time(self) -> int:
        return self._time

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def unpack_action(self):
        return (self._action, self._args)


class EventsHandler:
    def __init__(self, final_time: int, initial_events: List[Event] = list()) -> None:
        sort_events: Callable[[Event], Tuple[int, int]] = lambda x: (
            x.time,
            x.priority,
        )
        self._events: SortedSet = SortedSet(initial_events, key=sort_events)
        self._current_time = 0
        self._final_time = final_time

    def add(self, event: Event) -> bool:
        if event.time < self.current_time:
            raise Exception(f"Cannot send events to the past")
        if event.time > self._final_time:
            return False
        self._events.add(event)

        return True

    def next(self) -> List[Event]:
        event: Event = self._events.pop(0)
        self._current_time = event.time
        return self._next([event])

    def _next(self, next_events: List[Event]) -> List[Event]:
        if len(self._events) > 0 and self._current_time == self._events[0].time:
            event: Event = self._events.pop(0)
            return self._next(next_events + [event])
        return next_events

    @property
    def can_continue(self) -> bool:
        return self._current_time <= self._final_time and len(self._events) > 0

    @property
    def current_time(self) -> int:
        return self._current_time

    @property
    def final_time(self) -> int:
        return self._final_time


# e1 = Event(0, 1)
# e2 = Event(1, 1)
# e3 = Event(1, 2)

# el = EventList([e1, e2, e3])

# print(el.next().priority)
# print(el.next().priority)
# print(el.next().priority)
