from src.models.parking_status import ParkingStatus
from src.models.vehicles import Vehicle


class ParkingSlot:
    number: int
    status: ParkingStatus
    parked_vehicle: Vehicle

    def __init__(self, number: int):
        self.number = number
        self.status = ParkingStatus.EMPTY
        self.parked_vehicle = None

    def is_free(self):
        return self.status == ParkingStatus.EMPTY

    def assign_slot(self, vehicle: Vehicle):
        self.status = ParkingStatus.PARKED
        self.parked_vehicle = vehicle

    def vacant_slot(self):
        self.status = ParkingStatus.EMPTY
        self.parked_vehicle = None
