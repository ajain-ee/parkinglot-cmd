from src.models.parking_slot import ParkingSlot
from src.models.parking_statuses import ParkingStatuses
from src.models.vehicles import Vehicle


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
        self.is_vehicle_already_parked(vehicle)
        empty_spots[0].assign_slot(vehicle)
        self.log_message("Allocated slot number: {0}".format(empty_spots[0].number))

    def is_vehicle_already_parked(self, vehicle: Vehicle):
        for i, slot in enumerate(self.parking_slots):
            if slot.status is ParkingStatuses.PARKED and slot.parked_vehicle.registration_number == vehicle.registration_number:
                self.log_message(
                    "Vehicle with registration number {0} is already parked in Slot {1} , cannot reassign the Slot".format(
                        vehicle.registration_number, slot.number))
        return

    def vacant_from_spot(self, registration_number: str, parking_hours: int):
        if len(list(
                filter(
                    lambda x: x.parked_vehicle is not None and x.parked_vehicle.registration_number == registration_number,
                    self.parking_slots))) == 0:
            self.log_message("Registration Number {0} not found".format(registration_number))
            return

        slot = list(filter(lambda
                               x: x.status is ParkingStatuses.PARKED and x.parked_vehicle.registration_number == registration_number,
                           self.parking_slots))[0]
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
        self.log_message("Slot No. Registration No")
        non_empty_spots = self.get_parked_slots()
        for slot in non_empty_spots:
            self.log_message("{0}        {1}".format(slot.number, slot.parked_vehicle.registration_number))

    def get_parked_slots(self):
        return list(filter(lambda x: x.status == ParkingStatuses.PARKED, self.parking_slots))

    def get_vacant_slots(self):
        return list(filter(lambda x: x.status.value == ParkingStatuses.EMPTY.value, self.parking_slots))

    def log_message(self, message):
        print(message)
