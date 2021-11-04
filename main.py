from math import floor
from classes import Female, Male, Person
from typing import List, Callable
from random import random, uniform, randint
from events import Event, EventList

from events import EventList


def generate_max_kids():
    pass


# Needs to generate a Exponential Var
def generate_break_up_time() -> int:
    return randint(4, 36)


def event_wants_partner():
    pass


def event_partnerhip():
    pass


def event_breakup():
    pass


def event_pregnants():
    pass


def event_labourd():
    pass


def event_grow_old(population: List[Person], events: EventList) -> str:
    for person in population:
        person.increase_age(1 / 12)
    return ""


def event_die(population: List[Person], events: EventList) -> str:
    log: str = ""
    age_question: Callable[[Person, int, int], bool] = (
        lambda p, x, y: True if x <= p.age < y else False
    )
    prob_question: Callable[[Person, float, float, float], bool] = (
        lambda p, u0, u1, u2: True
        if (p.is_male and u0 < u1) or (p.is_female and u0 < u2)
        else False
    )
    remove_indexes: List[int] = []
    for index, person in enumerate(population):
        u = random()
        if (
            (age_question(person, 0, 12) and u < 0.25)
            or (age_question(person, 12, 45) and prob_question(person, u, 0.1, 0.15))
            or (age_question(person, 45, 78) and prob_question(person, u, 0.3, 0.35))
            or (age_question(person, 76, 125) and prob_question(person, u, 0.7, 0.65))
        ):
            remove_indexes.append(index)

    remove_indexes.reverse()
    for index in remove_indexes:
        person = population.pop(index)
        log += f"{person}: passed away\n"
        if person.has_partner:
            person.get_partner.break_up(generate_break_up_time())
    return log


def generate_popultaion(males: int, females: int):
    population: List[Person] = list()
    for _ in range(males):
        population.append(Male(name="Male", age=uniform(0, 100), max_kids=2))
    for _ in range(females):
        population.append(Female(name="Female", age=uniform(0, 100), max_kids=2))

    return population


def main(males: int, females: int):
    # Generate new population
    population: List[Person] = generate_popultaion(males, females)
    # Generate predefined inital Events
    initial_events: List[Event] = [Event(event_die, 12 * i, 5) for i in range(100)]
    initial_events += [Event(event_grow_old, i, 6) for i in range(100 * 12)]


def run_simul(population: List[Person], events: EventList):
    while events.can_continue:
        curr_event = events.next()
        log: str = curr_event.execute(population, events)
        if log != "":
            print(
                f"Month: {events.current_time%12} Year: {floor(events.current_time/12)}",
                log,
                sep="\n",
            )
    print("Simulation Ended")
    print(f"Remaining population {len(population)}")
