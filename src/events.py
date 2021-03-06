from math import log
from random import random
from typing import Callable, Dict

from person import Female, Male, Person
from event_handlers import Event, EventsHandler
from config import *

global people_produced
global total_wants_partner
global total_partners
global total_pregnancies
global total_labours
global total_widowing
global total_breakups
global total_deaths


def valid_event(event: Callable[..., str]) -> Callable[..., str]:
    def inner(*args: ...):
        try:
            return event(*args)
        except KeyError:
            return ""
    return inner


def uniform(a: float, b: float) -> float:
    u = random()
    return u * (b - a) + a


def int_uniform(a: float, b: float) -> int:
    return round(uniform(a, b))


def exponential(param: float) -> float:
    u = random()
    return -log(u) / param


def next_age_group(p: Person) -> int:
    age = p.age
    for year in AGE_RANK:
        if age < year:
            return year - age

    raise Exception(f"Internal error calculating a {p} age group")


def generate_max_kids() -> int:
    for amount, prob in enumerate([0.6, 0.75, 0.35, 0.2, 0.1]):
        u = random()
        if u < prob:
            return amount + 1

    u = random()
    if u < 0.05:
        return 1000

    return 0


def generate_time_alone(p: Person) -> int:
    age = p.age/12
    if 12 <= age < 15:
        return round(exponential(1 / 3))
    if 15 <= age < 35:
        return round(exponential(1 / 6))
    if 35 <= age < 45:
        return round(exponential(1 / 12))
    if 45 <= age < 60:
        return round(exponential(1 / 24))
    if 60 <= age < 125:
        return round(exponential(1 / 48))
    return SIMULATION_END


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


def time_of_death(person: Person):
    age = round(person.age / 12)
    u = random()

    prob: Callable[[Person, float, float, float], bool] = (
        lambda p, u0, u1, u2: True
        if (p.is_male and u0 < u1) or (p.is_female and u0 < u2)
        else False
    )

    if 0 <= age < 12 and u < 0.25:
        return int_uniform(0, 12 - age) * 12
    if 12 <= age < 45 and prob(person, u, 0.1, 0.15):
        return int_uniform(0, 45 - age) * 12
    if 45 <= age < 76 and prob(person, u, 0.3, 0.35):
        return int_uniform(0, 76 - age) * 12
    if 76 <= age < 125 and prob(person, u, 0.7, 0.65):
        return int_uniform(0, 125 - age) * 12
    if age >= 125:
        return 1

    return 2 * SIMULATION_END


def generate_initial_popultaion(m: int, f: int, events: EventsHandler):
    print("Setting up global vars")

    global people_produced
    global total_labours
    global total_widowing
    global total_partners
    global total_pregnancies
    global total_wants_partner
    global total_breakups
    global total_deaths

    people_produced = m + f
    total_labours = 0
    total_widowing = 0
    total_partners = 0
    total_pregnancies = 0
    total_wants_partner = 0
    total_breakups = 0
    total_deaths = 0

    print(f"Generating inital population {m} males, {f} females...")

    population: Dict[bytes, Person] = dict()
    for count in range(m + f):
        p = (
            Male("Male", int_uniform(0, 100) * 12, generate_max_kids(), id=count)
            if count < m
            else Female(
                "Female", int_uniform(0, 100) * 12, generate_max_kids(), id=count
            )
        )
        population[p.id] = p
        ultimate_demise = time_of_death(p)
        if ultimate_demise < SIMULATION_END:
            events.add(
                Event(
                    die_event,
                    events.current_time + ultimate_demise,
                    0,
                    population,
                    events,
                    p.id,
                    ultimate_demise,
                )
            )

        else:
            next_age = next_age_group(p)
            events.add(
                Event(
                    grow_old_event,
                    round(events.current_time + next_age),
                    2,
                    population,
                    events,
                    p.id,
                    next_age,
                )
            )

    print("Population generated")
    return population


def die_event(
    population: Dict[str, Person], events: EventsHandler, idx: str, ultimate_demise: int
):
    global total_deaths
    total_deaths += 1
    
    person = population[idx]
    person.increase_age(ultimate_demise)
    del population[idx]

    if person.has_partner:
        global total_widowing
        total_widowing += 1

        partner = person.get_partner
        partner_time_alone: int = events.current_time + generate_time_alone(partner)
        partner.break_up(partner_time_alone)
        events.add(
            Event(
                wants_partner_event,
                partner_time_alone + int_uniform(*WANT_PARTNER_RANGE),
                5,
                population,
                events,
                partner.id,
            )
        )

    return f"{person} died."


@valid_event
def grow_old_event(
    population: Dict[str, Person], events: EventsHandler, idx: str, time: int
):
    person = population[idx]
    person.increase_age(time + 1)

    if 12 * 12 <= person.age < 15 * 12:
        events.add(
            Event(
                wants_partner_event,
                events.current_time + int_uniform(*WANT_PARTNER_RANGE),
                5,
                population,
                events,
                idx,
            )
        )

    ultimate_demise = time_of_death(person)
    death_time = events.current_time + ultimate_demise
    if death_time < SIMULATION_END:
        events.add(
            Event(
                die_event,
                death_time,
                0,
                population,
                events,
                idx,
                ultimate_demise,
            )
        )
    else:
        next_age = next_age_group(person)
        events.add(
            Event(
                grow_old_event,
                events.current_time + next_age,
                2,
                population,
                events,
                idx,
                next_age,
            )
        )

    return ""


@valid_event
def wants_partner_event(population: Dict[str, Person], events: EventsHandler, idx: str):
    person = population[idx]

    if person.has_partner:
        return ""
    
    if person.wants_partner:
        raise Exception(f"{person} cannot want a partner again. Internal Error.")

    person.update_time_alone(events.current_time)
    age = person.age / 12
    u = random()
    if (
        (12 <= age < 15 and u < 0.6)
        or (15 <= age < 21 and u < 0.65)
        or (21 <= age < 35 and u < 0.8)
        or (35 <= age < 45 and u < 0.6)
        or (45 <= age < 60 and u < 0.5)
        or (60 <= age < 125 and u < 0.2)
    ):
        global total_wants_partner
        total_wants_partner += 1

        person.set_wants_partner()
        events.add(
            Event(
                partner_event,
                events.current_time + int_uniform(*PARTNER_RANGE),
                5,
                population,
                events,
                idx,
            )
        )
        return f"{person} is looking for a relationship"

    events.add(
        Event(
            wants_partner_event,
            events.current_time + int_uniform(*WANT_PARTNER_RANGE),
            3,
            population,
            events,
            idx
            )
        )
    return ""


@valid_event
def partner_event(population: Dict[bytes, Person], events: EventsHandler, idx: bytes):
    person = population[idx]
    if person.has_partner or not person.wants_partner:
        return ""
    # a person is selected by another partner events, and then dies
    # this person has an alone time needed to complete
    if person.update_time_alone(events.current_time) != 0:
        return ""

    for k in population:
        partner = population[k]
        if (
            (partner.is_male and person.is_male)
            or (partner.is_female and person.is_female)
        ) or not partner.wants_partner:
            continue

        u = random()
        diff = abs(person.age - partner.age) / 2
        if (
            (0 <= diff <= 5 and u < 0.45)
            or (5 < diff <= 10 and u < 0.4)
            or (10 < diff <= 15 and u < 0.35)
            or (15 < diff <= 20 and u < 0.25)
            or (20 < diff <= 100 and u < 0.15)
        ):
            global total_partners
            total_partners += 1

            person.set_partner(partner)
            partner.set_partner(person)
            female = person if person.is_female else partner
            male = person if person.is_male else partner
            events.add(
                Event(
                    get_pregnant_event,
                    events.current_time + int_uniform(*PREGNANT_RANGE),
                    3,
                    population,
                    events,
                    female.id,
                    male.id
                )
            )
            events.add(
                Event(
                    break_up_event,
                    events.current_time + int_uniform(*BREAK_UP_RANGE),
                    2,
                    population,
                    events,
                    female.id,
                )
            )
            return f"{person} and {partner} are joined in a relationship"

    events.add(
        Event(
            partner_event,
            events.current_time + int_uniform(*PARTNER_RANGE),
            5,
            population,
            events,
            person.id,
        )
    )
    return ""


@valid_event
def get_pregnant_event(
        population: Dict[bytes, Person],
        events: EventsHandler,
        female_idx: bytes,
        male_idx: bytes
    ):
    female = population[female_idx]
    male = female.get_partner

    if not isinstance(female, Female):
        raise Exception("Cannot get a male pregnant")
    
    # Female is already pregnant by a previous male
    if female.is_pregnant and male.id == male_idx:
        return ""
    
    # A female cannot get pregnat with a male she is not
    # currently with
    if female.has_partner and male.id != male_idx:
        return ""
    if not female.want_kids or not male.want_kids or not female.has_partner:
        return ""


    u = random()
    age = female.age / 12
    if (
        (12 <= age < 15 and u < 0.2)
        or (15 <= age < 21 and u < 0.45)
        or (21 <= age < 35 and u < 0.8)
        or (35 <= age < 45 and u < 0.4)
        or (45 <= age < 60 and u < 0.2)
        or (60 <= age < 125 and u < 0.05)
    ):
        global total_pregnancies
        total_pregnancies += 1

        female.set_pregnant(generate_baby_amount())
        events.add(
            Event(labour_event, events.current_time + 9, 0, population, events, female_idx, male_idx)
        )
        return f"{female} got pregnant"

    events.add(
        Event(
            get_pregnant_event,
            events.current_time + int_uniform(*PREGNANT_RANGE),
            5,
            population,
            events,
            female_idx,
            male_idx
        )
    )
    return ""


@valid_event
def labour_event(population: Dict[bytes, Person], events: EventsHandler, female_idx: bytes, male_idx: bytes):
    female = population[female_idx]
    if not isinstance(female, Female):
        raise Exception("Cannot get a male to labour you sick bastard!")
    global total_labours
    total_labours += 1

    global people_produced
    new_kids = female.labour()
    for i in range(1, new_kids + 1):
        u = random()
        child: Person
        if u < 0.5:
            child = Male("Male", 1, generate_max_kids(), people_produced + i)
        else:
            child = Female("Female", 1, generate_max_kids(), people_produced + i)

        ultimate_demise = time_of_death(child)
        if ultimate_demise < SIMULATION_END:
            events.add(
                Event(
                    die_event,
                    events.current_time + ultimate_demise,
                    0,
                    population,
                    events,
                    child.id,
                    ultimate_demise,
                )
            )
        else:
            next_age = next_age_group(child)
            events.add(
                Event(
                    grow_old_event,
                    events.current_time + next_age,
                    2,
                    population,
                    events,
                    child.id,
                    next_age,
                )
            )
        population[child.id] = child

    people_produced = people_produced + new_kids

    if female.has_partner and female.get_partner.id == male_idx:
        events.add(
            Event(
                get_pregnant_event,
                events.current_time + int_uniform(*PREGNANT_REST_RANGE),
                5,
                population,
                events,
                female_idx,
                male_idx
            )
        )
    return f"{female} brought to life {new_kids} kids"


@valid_event
def break_up_event(population: Dict[str, Person], events: EventsHandler, idx: str):
    person = population[idx]
    if not person.has_partner:
        return ""

    u = random()
    if u < 0.2:
        global total_breakups
        total_breakups += 1

        partner = person.get_partner
        person_time_alone: int = events.current_time + generate_time_alone(person)
        partner_time_alone: int = events.current_time + generate_time_alone(partner)
        person.break_up(person_time_alone)
        partner.break_up(partner_time_alone)
         
        events.add(
            Event(
                wants_partner_event,
                person_time_alone + int_uniform(*WANT_PARTNER_RANGE),
                5,
                population,
                events,
                person.id,
            )
        )
        events.add(
            Event(
                wants_partner_event,
                partner_time_alone + int_uniform(*WANT_PARTNER_RANGE),
                5,
                population,
                events,
                partner.id,
            )
        )
        return f"{person} and {partner} broke up"
    else:
        events.add(
            Event(
                break_up_event,
                events.current_time + int_uniform(*BREAK_UP_RANGE),
                2,
                population,
                events,
                idx,
            )
        )

    return ""


# Select all not interested parties of population in having sexual intercourse and
# motivates them. Only use once at the begining.
def break_the_ice(population: Dict[bytes, Person], events: EventsHandler):
    print("Seeding relationship interest between people older than 12 years ...")
    filtered_popultation = [
        key
        for key in population
        if population[key].age >= 12*12
        and not population[key].wants_partner
        and not population[key].has_partner
    ]
    for idx in filtered_popultation:
        events.add(
            Event(
                wants_partner_event,
                int_uniform(*WANT_PARTNER_RANGE),
                5,
                population,
                events,
                idx,
            )
        )
    print("Done")
