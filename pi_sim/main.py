#!/usr/bin/env python3

import asyncio
from typing_extensions import get_args
from pymavlink import mavutil
import time
import sys
from CUSP_camera import *
from CUSP_trigger import *
from mock_gps import *
import json
# from multiprocessing import Process
from threading import Thread, Lock

"""
Main program to run CUSP
"""

def poll_GPS(periodSeconds, GPS):
    # Handle polling GPS data here

    # mocked variables
    mock_latitude: float = 29.65
    mock_longitude: float = -82.30
    mock_altitude: float = 30.0

    while True:
        # GPS_dev.fetch_GPS_data()
        mock_latitude += 0.001

        GPS.set_mock_gps_data(mock_latitude, mock_longitude, mock_altitude)

        # might have to bump up frequency depending on how fast it's flying
        sleep(periodSeconds)


def main():

    # Activate connection to flight controller

    """
    the_connection = mavutil.mavlink_connection(
        "tcp:127.0.0.1:5760", baud=57600, source_system=1, source_component=2
    )
    # the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14550', baud=57600, source_system=1, source_component=2)
    print("Creating connection...")

    the_connection.wait_heartbeat()
    print(
        "Heartbeat from system (system %u component %u)"
        % (the_connection.target_system, the_connection.target_component)
    )


    # Initialize callback for PWM triggering
    PWM_init()
    Overlap_init()

    GPS_init()
    """

    # GPS_dev = GPSClass()

    GPSprocess = Thread(target=poll_GPS, args=(0.1,GPS_dev,))
    GPSprocess.start()

    configJSON = open("../Web_App/form_data.json")

    configData = json.load(configJSON)

    print(configData)
    # while True:
        # print(GPS_dev.get_GPS_data())
        # sleep(0.1)
    # capture_rgb()


if __name__ == "__main__":
    main()
