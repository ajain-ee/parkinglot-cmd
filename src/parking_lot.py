from src.models.parking_slot import ParkingSlot
from src.models.parking_status import ParkingStatus
from src.models.vehicles import Vehicle


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#  make singleton later on
class ParkingLot:

    def __init__(self, name, slots):
        self.name: str = name
        self.parking_slots: [ParkingSlot] = []

        for number in range(slots):
            slot_number = number + 1
            self.parking_slots.append(ParkingSlot(slot_number))

        print("Created parking lot with {0} slots".format(slots))

    def park_on_spot(self, vehicle: Vehicle):
        empty_spots = list(filter(lambda x: x.status == ParkingStatus.EMPTY, self.parking_slots))
        if len(empty_spots) == 0:
            print("Sorry, parking lot is full")
            raise RuntimeError("Sorry, parking lot is full")
        print("Allocated slot number: {0}".format(empty_spots[0].number))
        empty_spots[0].assign_slot(vehicle)

    def unpark_from_spot(self, slot_number):
        pass
