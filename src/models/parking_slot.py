from src.models.parking_statuses import ParkingStatuses
from src.models.vehicles import Vehicle


class ParkingSlot:
    number: int
    status: ParkingStatuses
    parked_vehicle: Vehicle

    def __init__(self, number: int):
        self.number = number
        self.status = ParkingStatuses.EMPTY
        self.parked_vehicle = None

    def is_free(self):
        return self.status == ParkingStatuses.EMPTY

    def assign_slot(self, vehicle: Vehicle):
        self.status = ParkingStatuses.PARKED
        self.parked_vehicle = vehicle

    def vacant_slot(self):
        self.status = ParkingStatuses.EMPTY
        self.parked_vehicle = None
