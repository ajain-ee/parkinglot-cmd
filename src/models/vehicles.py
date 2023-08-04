import abc


class Vehicle(metaclass=abc.ABCMeta):
    def __init__(self, registration_number: str):
        self.registration_number: str = registration_number


class Car(Vehicle):
    pass
