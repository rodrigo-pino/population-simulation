from typing import Dict
from event_handlers import EventsHandler
from config import SIMULATION_END
from person import Person
import sys

from events import (
    break_the_ice,
    generate_initial_popultaion,
)

import events as global_vars


def run_simul(events: EventsHandler, population: Dict[bytes, Person]):
    print(f"Starting Simulation with {len(population)}")

    while events.can_continue:
        log: str = ""
        for event in events.next():
            event_log = event.execute()
            if event_log != "":
                log += event_log + "\n"

        if log != "":
            print(
                f"========= Year: {int(events.current_time / 12)}, "
                f"Month: {events.current_time % 12 + 1} "
                f"Population Size: {len(population)} ========="
            )
            print(log)

    print(
        f"######### Simulation Ended with {len(population)} people remaining #########"
    )
    print(f"Interests in relationships: {global_vars.total_wants_partner}")
    print(f"Relationships: {global_vars.total_partners}")
    print(f"Pregnancies: {global_vars.total_pregnancies}")
    print(f"Labours: {global_vars.total_labours}")
    print(f"Break ups: {global_vars.total_breakups}")
    print(f"Deaths: {global_vars.total_deaths}")
    print(f"People Widowed: {global_vars.total_widowing}")


def main():
    argv = sys.argv
    m = int(argv[1])
    f = int(argv[2])

    events = EventsHandler(SIMULATION_END)
    population = generate_initial_popultaion(m, f, events)
    break_the_ice(population, events)
    run_simul(events, population)


main()
