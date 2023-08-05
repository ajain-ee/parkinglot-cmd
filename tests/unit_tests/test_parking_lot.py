import unittest
from unittest import mock

import pytest

from src.parking_lot import ParkingLot
from src.models.vehicles import Car
from src.models.parking_statuses import ParkingStatuses


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
        assert pl.parking_slots[0].status == ParkingStatuses.PARKED
        assert pl.parking_slots[0].parked_vehicle == car

    def test_parking_lot_should_fill_next_available_spot(self):
        pl = ParkingLot("testparking", 3)

        car1 = Car("KA-01-HH-1234")
        pl.parking_slots[0].assign_slot(car1)

        car2 = Car("KA-01-HH-1235")
        pl.park_on_spot(car2)

        assert pl.parking_slots[0].status == ParkingStatuses.PARKED
        assert pl.parking_slots[0].parked_vehicle == car1
        assert pl.parking_slots[1].status == ParkingStatuses.PARKED
        assert pl.parking_slots[1].parked_vehicle == car2
        assert pl.parking_slots[2].status == ParkingStatuses.EMPTY
        assert pl.parking_slots[2].parked_vehicle is None

    def test_parking_lot_should_not_reassign_the_slot_to_same_car(self):
        pl = ParkingLot("testparking", 2)

        car1 = Car("first_car")
        pl.park_on_spot(car1)

        assert pl.parking_slots[0].status == ParkingStatuses.PARKED
        assert pl.parking_slots[0].parked_vehicle == car1

        with pytest.raises(RuntimeError) as ae:
            pl.park_on_spot(car1)

    def test_parking_lot_should_raise_exception_if_no_slot_is_available(self):
        pl = ParkingLot("testparking", 3)

        pl.parking_slots[0].assign_slot(Car("KA-01-HH-1234"))
        pl.parking_slots[1].assign_slot(Car("KA-01-HH-1235"))
        pl.parking_slots[2].assign_slot(Car("KA-01-HH-1236"))

        with pytest.raises(RuntimeError) as ae:
            pl.park_on_spot(Car("KA-01-HH-1237"))

        assert str(ae.value) == "Sorry, parking lot is full"

    def test_parking_lot_should_empty_slot_if_unpark(self):
        pl = ParkingLot("testparking", 3)
        car1 = Car("KA-01-HH-1234")
        car2 = Car("KA-01-HH-1235")

        pl.park_on_spot(car1)
        pl.park_on_spot(car2)

        pl.vacant_from_spot("KA-01-HH-1235", 2)

        assert pl.parking_slots[0].status == ParkingStatuses.PARKED
        assert pl.parking_slots[0].parked_vehicle == car1

        assert pl.parking_slots[1].status == ParkingStatuses.EMPTY
        assert pl.parking_slots[1].parked_vehicle is None

        assert pl.parking_slots[2].status == ParkingStatuses.EMPTY
        assert pl.parking_slots[2].parked_vehicle is None

    def test_parking_charges_for_less_than_2_hours(self):
        pl = ParkingLot("testparking", 2)
        car1 = Car("KA-01-HH-1234")
        car2 = Car("KA-01-HH-1235")
        pl.park_on_spot(car1)
        pl.park_on_spot(car2)
        parking_charges = pl.vacant_from_spot(car1.registration_number, 2)
        assert parking_charges == 10

        parking_charges = pl.vacant_from_spot(car2.registration_number, 1)
        assert parking_charges == 10

    def test_parking_charges_for_more_than_2_hours(self):
        pl = ParkingLot("testparking", 2)
        car1 = Car("KA-01-HH-1234")
        car2 = Car("KA-01-HH-1235")
        pl.park_on_spot(car1)
        pl.park_on_spot(car2)

        parking_charges = pl.vacant_from_spot(car1.registration_number, 3)
        assert parking_charges == 20

        parking_charges = pl.vacant_from_spot(car1.registration_number, 5)
        assert parking_charges == 40

    def test_get_vacant_slots(self):
        pl = ParkingLot("testparking", 2)
        pl.park_on_spot(Car("KA-01-HH-1234"))

        slots = pl.get_vacant_slots()
        assert len(slots) == 1

    def test_get_parked_slots(self):
        pl = ParkingLot("testparking", 2)
        pl.park_on_spot(Car("KA-01-HH-1234"))

        slots = pl.get_parked_slots()
        assert len(slots) == 1
        assert slots[0].number == 1
        assert slots[0].parked_vehicle.registration_number == "KA-01-HH-1234"

    @mock.patch('src.parking_lot.ParkingLot.log_message', return_value=None)
    def test_parking_status_when_parking_lot_full(self, mock_log_message):
        pl = ParkingLot("testparking", 1)
        pl.park_on_spot(Car("KA-01-HH-1234"))

        pl.parking_status()

        mock_log_message.assert_called_once_with("Sorry, parking lot is full")

    @mock.patch('src.parking_lot.ParkingLot.log_message', return_value=None)
    def test_parking_status_when_parking_have_vacant_lots(self, mock_log_message):
        pl = ParkingLot("testparking", 4)
        pl.park_on_spot(Car("KA-01-HH-1234"))
        pl.park_on_spot(Car("KA-01-HH-1235"))
        pl.park_on_spot(Car("KA-01-HH-1236"))

        pl.parking_status()

        mock_log_message.assert_has_calls(
            [
                mock.call("Slot No. Registration No"),
                mock.call("1 KA-01-HH-1234"),
                mock.call("2 KA-01-HH-1235"),
                mock.call("3 KA-01-HH-1236"),
            ])
