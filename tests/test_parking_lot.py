import unittest

import pytest

from src.parking_lot import ParkingLot
from src.models.vehicles import Car
from src.models.parking_status import ParkingStatus


class ParkingLotTest(unittest.TestCase):

    def test_create_parking_with_1_slot(self):
        pl = ParkingLot("testparking", 1)
        assert len(pl.parking_slots) == 1

    def test_create_parking_with_5_slots(self):
        pl = ParkingLot("testparking", 5)
        assert len(pl.parking_slots) == 5
        assert pl.parking_slots[0].number == 1
        assert pl.parking_slots[1].number == 2
        assert pl.parking_slots[2].number == 3
        assert pl.parking_slots[3].number == 4
        assert pl.parking_slots[4].number == 5

    # def test_only_single_instance_of_parking_lot(self):
    #     pl1 = ParkingLot("testparking")
    #     pl2 = ParkingLot("testparking1")
    #
    #     assert pl1 == pl2
    #     assert pl1.name == "testparking"
    #
    # def test_parking_lot_should_not_alter_spots(self):
    #     pl1 = ParkingLot("testparking")
    #     pl2 = ParkingLot("testparking1")
    #
    #     pl1.create(2)
    #     pl2.create(3)
    #     assert len(pl1.parking_slots) == 2
    #     assert len(pl2.parking_slots) == 2
    #     assert pl1.parking_slots[0].number == 1
    #     assert pl1.parking_slots[1].number == 2
    #     assert pl2.parking_slots[0].number == 1
    #     assert pl2.parking_slots[1].number == 2

    def test_parking_lot_should_fill_only_available_spot(self):
        pl = ParkingLot("testparking", 1)
        car = Car("KA-01-HH-1234")
        pl.park_on_spot(car)
        assert pl.parking_slots[0].status == ParkingStatus.PARKED
        assert pl.parking_slots[0].parked_vehicle == car

    def test_parking_lot_should_fill_next_available_spot(self):
        pl = ParkingLot("testparking", 3)

        car1 = Car("KA-01-HH-1234")
        pl.parking_slots[0].assign_slot(car1)

        car2 = Car("KA-01-HH-1235")
        pl.park_on_spot(car2)

        assert pl.parking_slots[0].status == ParkingStatus.PARKED
        assert pl.parking_slots[0].parked_vehicle == car1
        assert pl.parking_slots[1].status == ParkingStatus.PARKED
        assert pl.parking_slots[1].parked_vehicle == car2
        assert pl.parking_slots[2].status == ParkingStatus.EMPTY
        assert pl.parking_slots[2].parked_vehicle is None


    def test_parking_lot_should_raise_exception_if_no_slot_is_available(self):
        pl = ParkingLot("testparking", 3)

        pl.parking_slots[0].assign_slot(Car("KA-01-HH-1234"))
        pl.parking_slots[1].assign_slot(Car("KA-01-HH-1235"))
        pl.parking_slots[2].assign_slot(Car("KA-01-HH-1236"))

        with pytest.raises(RuntimeError) as ae:
            pl.park_on_spot(Car("KA-01-HH-1237"))

        assert str(ae.value) == "Sorry, parking lot is full"

    # def test_parking_lot_should_empty_slot_if_unpark(self):
    #     pl = ParkingLot("testparking", 3)
    #
    #     pl.parking_slots[0].update_parking_status(ParkingStatus.PARKED)
    #
    #     pl.unpark_from_spot(2, )
