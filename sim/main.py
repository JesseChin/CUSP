# NOTICE: Deprecated


#!/usr/bin/env python3

import asyncio
from typing_extensions import get_args
from pymavlink import mavutil
import time
import sys
from mock_camera import *
from mock_trigger import *
from CUSP_gps import *

"""
Main program to run CUSP
"""


async def poll_GPS():
    # Handle polling GPS data here
    while True:
        fetch_GPS_data()
        # might have to bump up frequency depending on how fast it's flying
        await asyncio.sleep(0.1)


async def main():
    # Activate connection to flight controller

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

    await asyncio.gather(poll_GPS)


if __name__ == "__main__":
    asyncio.run(main())
