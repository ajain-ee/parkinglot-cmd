import argparse

from src.models.vehicles import Car
from src.parking_lot import ParkingLot


def start_ticket_system(filepath):
    file1 = open(filepath, 'r')
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        line.strip()
        split = line.split(" ")
        if split[0] == "create":
            parkinglot = ParkingLot("test", int(split[1].strip()))
        if split[0] == "park":
            parkinglot.park_on_spot(Car(split[1].strip()))
        if split[0] == "leave":
            parkinglot.vacant_from_spot(split[1], int(split[2].strip()))
        if split[0] == "status":
            parkinglot.parking_status()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--parking-simulation-file', dest='parking-simulation-file')

    start_ticket_system("/Users/anujjain/workspace/parkinglot-cmd/tests/integration_tests/test_command.txt")
