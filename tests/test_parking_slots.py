import unittest
from src.models.parking_slot import ParkingSlot
from src.models.parking_status import ParkingStatus
from src.models.vehicles import Car


class ParkingSlotTest(unittest.TestCase):

    def test_parking_slot_default_values(self):
        slot = ParkingSlot(1)
        assert slot.status == ParkingStatus.EMPTY
        assert slot.parked_vehicle is None

    def test_assign_slot_should_assign_slot_to_car(self):
        slot = ParkingSlot(1)
        car = Car("1111111")
        slot.assign_slot(car)

        assert slot.parked_vehicle == car
        assert slot.status == ParkingStatus.PARKED

    def test_vacant_slot_should_reset_slot_status(self):
        slot = ParkingSlot(1)
        slot.vacant_slot()

        assert slot.parked_vehicle is None
        assert slot.status == ParkingStatus.EMPTY

    def test_parking_slot_is_vacant(self):
        slot = ParkingSlot(1)
        assert slot.is_free() is True

        slot = ParkingSlot(1)
        slot.assign_slot(Car("1111111"))
        assert slot.is_free() is False
