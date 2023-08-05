from src.models.parking_slot import ParkingSlot
from src.models.parking_statuses import ParkingStatuses
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

        self.log_message("Created parking lot with {0} slots".format(slots))

    def park_on_spot(self, vehicle: Vehicle):
        empty_spots = self.get_vacant_slots()
        if len(empty_spots) == 0:
            self.log_message("Sorry, parking lot is full")
            return
        self.log_message("Allocated slot number: {0}".format(empty_spots[0].number))
        self.is_vehicle_already_parked(vehicle)
        empty_spots[0].assign_slot(vehicle)

    def is_vehicle_already_parked(self, vehicle: Vehicle):
        for i, slot in enumerate(self.parking_slots):
            if slot.status is ParkingStatuses.PARKED and slot.parked_vehicle.registration_number == vehicle.registration_number:
                self.log_message(
                    "Vehicle with registration number {0} is already parked in Slot {1} , cannot reassign the Slot")

    def vacant_from_spot(self, registration_number: str, parking_hours: int):
        for vehicle in list(map(lambda x: x.parked_vehicle)):
            
        for i, slot in enumerate(self.parking_slots):
            if slot.status is ParkingStatuses.PARKED and slot.parked_vehicle.registration_number == registration_number:
                slot.vacant_slot()

        minimum_parking_charges = 10
        if parking_hours <= 2:
            self.log_message(
                "Registration Number {0} from Slot {1} has left with Charge {2}".format(registration_number,
                                                                                        slot.number,
                                                                                        minimum_parking_charges))
            return minimum_parking_charges
        else:
            total_charges = minimum_parking_charges + (parking_hours - 2) * 10
            self.log_message(
                "Registration Number {0} from Slot {1} has left with Charge {2}".format(registration_number,
                                                                                        slot.number,
                                                                                        total_charges))
            return total_charges

    def parking_status(self):
        empty_spots = self.get_vacant_slots()

        if len(empty_spots) == 0:
            self.log_message("Sorry, parking lot is full")
        else:
            self.log_message("Slot No. Registration No")
            non_empty_spots = self.get_parked_slots()
            for slot in non_empty_spots:
                self.log_message("{0} {1}".format(slot.number, slot.parked_vehicle.registration_number))

    def get_parked_slots(self):
        non_empty_spots = list(filter(lambda x: x.status == ParkingStatuses.PARKED, self.parking_slots))
        return non_empty_spots

    def get_vacant_slots(self):
        return list(filter(lambda x: x.status == ParkingStatuses.EMPTY, self.parking_slots))
        return empty_spots

    def log_message(self, message):
        print(message)
