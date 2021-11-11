from math import floor
from classes import Female, Male, Person
from typing import List, Callable, Set
from random import random, uniform
from events import Event, EventList

from events import EventList


def generate_max_kids() -> int:
    return 10


def generate_baby_amount() -> int:
    u = random()
    if u < 0.7:
        return 1
    if u < 0.7 + 0.18:
        return 2
    if u < 0.7 + 0.18 + 0.06:
        return 3
    if u < 0.7 + 0.18 + 0.10:
        return 4
    return 5


def generate_break_up_time(age: float) -> int:
    # u = random()
    # exponential dist
    # pram
    return 3


def event_wants_partner(population: List[Person], events: EventList) -> str:
    log: str = ""
    filtered_population = [
        person
        for person in population
        if not person.wants_partner
        and not person.has_partner
        and person.age >= 12
        and person.update_time_alone(events.current_time) == 0
    ]
    for person in filtered_population:
        u = random()
        age = person.age
        if (
            (12 < age < 15 and u < 0.6)
            or (15 < age < 21 and u < 0.65)
            or (21 < age < 35 and u < 0.8)
            or (35 < age < 45 and u < 0.6)
            or (45 < age < 60 and u < 0.5)
            or (60 < age < 125 and u < 0.2)
        ):
            person.set_wants_partner()
            log += f"{person} is interested in a relationships\n"
    return log


def event_partnerhip(population: List[Person], events: EventList) -> str:
    log: str = ""
    male_population: List[Person] = []
    female_population: List[Person] = []
    for person in population:
        if person.wants_partner:
            if person.has_partner:
                raise Exception("The unthinkable has happened")
            if person.is_female:
                female_population.append(person)
            else:
                male_population.append(person)
    taken_females: Set[int] = set()
    for male in male_population:
        for index, female in enumerate(female_population):
            if index in taken_females:
                continue
            u = random()
            diff = abs(male.age - female.age)
            if (
                (0 <= diff <= 5 and u < 0.45)
                or (5 < diff <= 10 and u < 0.4)
                or (10 < diff <= 15 and u < 0.35)
                or (15 < diff <= 20 and u < 0.25)
                or (20 < diff <= 100 and u < 0.15)
            ):
                male.set_partner(female)
                female.set_partner(male)
                log += f"{male} is in a relationships with {female}\n"
                taken_females.add(index)
                break

    return log


def event_breakup(population: List[Person], events: EventList) -> str:
    log: str = ""
    partnered_male_population = [
        person for person in population if person.is_male and person.has_partner
    ]
    for male in partnered_male_population:
        u = random()
        if u < 0.2:
            female = male.get_partner
            female.break_up(generate_break_up_time(female.age))
            male.break_up(generate_break_up_time(female.age))
            log += f"{female} and {male} broke up\n"

    return log


def event_pregnants(population: List[Person], events: EventList) -> str:
    log: str = ""
    partnered_female_population = [
        person
        for person in population
        if isinstance(person, Female)
        and person.has_partner
        and not person.is_pregnant
        and person.want_kids
        and person.get_partner.want_kids
    ]
    someone_got_pregnant = False
    for female in partnered_female_population:
        u = random()
        age = female.age
        if (
            (12 < age < 15 and u < 0.2)
            or (15 < age < 21 and u < 0.45)
            or (21 < age < 35 and u < 0.8)
            or (35 < age < 45 and u < 0.4)
            or (45 < age < 60 and u < 0.2)
            or (60 < age < 125 and u < 0.05)
        ):
            someone_got_pregnant = True
            female.set_pregnant(generate_baby_amount())
            log += f"{female} got pregnant\n"
    if someone_got_pregnant:
        events.add(Event(event_labour, events.current_time + 9, 0))
    return log


def event_labour(population: List[Person], events: EventList) -> str:
    log: str = ""
    pregnant_population = [
        person
        for person in population
        if isinstance(person, Female) and person.is_pregnant
    ]
    if len(pregnant_population) == 0:
        return ""
    total_new_kids = 0
    for female in pregnant_population:
        total_new_kids += female.labour()
        log += f"{female} went into labour\n"

    log += f"{total_new_kids} were borned (Population increase to {len(population) + total_new_kids})\n"
    new_little_people: List[Person] = []
    for _ in range(total_new_kids):
        u = random()
        if u < 0.5:
            new_little_people.append(Male("Boy", 0, generate_max_kids()))
        else:
            new_little_people.append(Female("Girl", 0, generate_max_kids()))

    for kid in new_little_people:
        population.append(kid)
    return log


def event_grow_old(population: List[Person], events: EventList) -> str:
    for person in population:
        person.increase_age(1 / 12)
    return ""


def event_die(population: List[Person], events: EventList) -> str:
    log: str = ""

    prob_question: Callable[[Person, float, float, float], bool] = (
        lambda p, u0, u1, u2: True
        if (p.is_male and u0 < u1) or (p.is_female and u0 < u2)
        else False
    )

    remove_indexes: List[int] = []
    for index, person in enumerate(population):
        u = random()
        age = person.age
        if (
            (0 < age < 12 and u < 0.25)
            or (12 < age < 45 and prob_question(person, u, 0.1, 0.15))
            or (45 < age < 76 and prob_question(person, u, 0.3, 0.35))
            or (76 < age < 125 and prob_question(person, u, 0.7, 0.65))
        ):
            remove_indexes.append(index)

    remove_indexes.reverse()
    for index in remove_indexes:
        person = population.pop(index)
        log += f"{person}: passed away\n"
        if person.has_partner:
            partner = person.get_partner
            partner.break_up(generate_break_up_time(partner.age))
    return log


def generate_popultaion(males: int, females: int):
    population: List[Person] = list()
    for _ in range(males):
        population.append(
            Male(name="Male", age=uniform(0, 100), max_kids=generate_max_kids())
        )
    for _ in range(females):
        population.append(
            Female(name="Female", age=uniform(0, 100), max_kids=generate_max_kids())
        )

    return population


def main(males: int, females: int):
    # Generate new population
    # population: List[Person] = generate_popultaion(males, females)
    # Generate predefined inital Events
    initial_events: List[Event] = [Event(event_die, 12 * i, 5) for i in range(100)]
    initial_events += [Event(event_grow_old, i, 6) for i in range(100 * 12)]


def run_simul(population: List[Person], events: EventList):
    while events.can_continue:
        log: str = ""
        for curr_event in events.next():
            log += curr_event.execute(population, events)
        if log != "":
            print(
                f"Month: {events.current_time%12} Year: {floor(events.current_time/12)} "
                f"Current Pop: {len(population)}",
                log,
                sep="\n",
            )
    print("Simulation Ended")
    print(f"Remaining population {len(population)}")
