import argparse
from pathlib import Path

from src.models.vehicles import Car
from src.parking_lot import ParkingLot


def start_ticket_system(filepath):
    file1 = open(filepath, 'r')
    lines = file1.readlines()

    for line in lines:
        line.strip()
        if "" != line.strip():
            split = line.split(" ")
            base_command = split[0].strip()
            if base_command == "create":
                parkinglot = ParkingLot("test", int(split[1].strip()))
            if base_command == "park":
                parkinglot.park_on_spot(Car(split[1].strip()))
            if base_command == "leave":
                parkinglot.vacant_from_spot(split[1].strip(), int(split[2].strip()))
            if base_command == "status":
                parkinglot.parking_status()


if __name__ == '__main__':

    def validate_file(arg):
        if (file := Path(arg)).is_file():
            return file
        else:
            raise FileNotFoundError(arg)


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-file", dest="config", type=validate_file, help="Input file path for parking lot system", required=True
    )
    args = parser.parse_args()

    start_ticket_system(args.config)
