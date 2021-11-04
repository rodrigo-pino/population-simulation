from classes import Female, Male, Person
from typing import List
from random import random, uniform


def generate_max_kids():
    pass


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


def event_die():
    pass


def generate_popultaion(males: int, females: int):
    population: List[Person] = list()
    for _ in range(males):
        population.append(Male(name="Male", age=uniform(0, 100), max_kids=2))
    for _ in range(females):
        population.append(Female(name="Female", age=uniform(0, 100), max_kids=2))

    return population


def main(males: int, females: int):
    population: List[Person] = generate_popultaion(males, females)
