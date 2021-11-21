from event_handlers import EventsHandler
from events import (
    break_the_ice,
    generate_initial_popultaion,
)
from config import SIMULATION_END

from main import run_simul


def test_base(m: int, f: int):
    events = EventsHandler(SIMULATION_END)
    population = generate_initial_popultaion(m, f, events)
    run_simul(events, population)


def test_wants(m: int, f: int):
    events = EventsHandler(SIMULATION_END)
    population = generate_initial_popultaion(m, f, events)
    break_the_ice(population, events)
    run_simul(events, population)


test_wants(10, 10)
