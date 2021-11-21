from __future__ import annotations
from hashlib import md5


class Person:
    def __init__(self, name: str, age: int, max_kids: int, id: int) -> None:
        self._name: str = name
        self._age: int = age
        self._max_kids: int = max_kids
        self._wants_partner: bool = False
        self._partnered: bool = False
        self._partner: Person
        self._time_alone: int = 0
        self._children: int = 0
        self._id: int = id

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def id(self) -> bytes:
        return md5(str(self.name + str(self._id)).encode()).digest()

    @property
    def wants_partner(self):
        return self._wants_partner

    @property
    def has_partner(self):
        return self._partnered

    @property
    def get_partner(self):
        return self._partner

    @property
    def want_kids(self):
        return self._children < self._max_kids

    def increase_age(self, time: int):
        self._age += time

    def set_wants_partner(self):
        if self._age / 12 < 12:
            raise Exception(f"{self.name} is too young to want a partner")
        if self._wants_partner:
            raise Exception(f"{self.name} already wants a partner.")
        if self._partnered:
            raise Exception(f"{self.name} already has a partner.")
        if self._time_alone != 0:
            raise Exception(f"{self.name} is recovering from past relationships.")
        self._wants_partner = True

    def set_partner(self, partner: Person):
        if self._partnered:
            raise Exception(
                f"{self.name} is already partnered with {self._partner.name}"
            )
        if not self._wants_partner:
            raise Exception(f"{self} is not looking for a partner")
        if (self.is_female and partner.is_female) or (self.is_male and partner.is_male):
            raise Exception(f"Simulation does not aloud same sex relationships")
        self._wants_partner = False
        self._partnered = True
        self._partner: Person = partner

    def break_up(self, time: int) -> None:
        if not self._partnered:
            raise Exception(f"{self.name} cannot break up without a partner")
        self._partnered = False
        self._time_alone = time

    def update_time_alone(self, time: int) -> int:
        self._time_alone = max(self._time_alone - time, 0)
        return self._time_alone

    @property
    def is_female(self) -> bool:
        raise NotImplementedError()

    @property
    def is_male(self) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.name}, age {int(self.age/12)}, {'married' if self._partnered else 'single'}, children {self._children}"

    def __repr__(self) -> str:
        return str(self)


class Female(Person):
    def __init__(self, name: str, age: int, max_kids: int, id: int) -> None:
        super().__init__(name, age, max_kids, id)
        self._pregnant_kids = 0
        self._partner: Male
        self._kids_parent: Male

    @property
    def is_pregnant(self):
        return self._pregnant_kids > 0

    def set_pregnant(self, kids_count: int):
        if not self.has_partner:
            raise Exception(f"{self.name} is not partenred with anyone")
        if self.is_pregnant:
            raise Exception(f"{self.name} is already pregnant")
        if not self.want_kids:
            raise Exception(f"{self.name} want's no more kids")

        self._pregnant_kids = kids_count
        self._kids_parent = self._partner

    def labour(self) -> int:
        new_little_people = self._pregnant_kids
        self._children += new_little_people
        self._kids_parent._children += new_little_people

        self._pregnant_kids = 0
        return new_little_people

    @property
    def is_female(self):
        return True

    @property
    def is_male(self):
        return False


class Male(Person):
    def __init__(self, name: str, age: int, max_kids: int, id: int) -> None:
        super().__init__(name, age, max_kids, id)
        self._partner: Female

    @property
    def is_female(self):
        return False

    @property
    def is_male(self):
        return True
