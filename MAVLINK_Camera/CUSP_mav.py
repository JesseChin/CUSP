#!/usr/bin/env python3

# We should be using this for MAV communication to modularize our code more, but
# currently using MAVLink in global context

from pymavlink import mavutil

from threading import Thread, Lock


class MAVClass:
    GPSmutex = Lock()

    def __init__(self, source, baudrate) -> None:
        master = mavutil.mavlink_connection(
            source, baud=baudrate, source_system=1, source_component=2
        )
        master.wait_heartbeat()


MAV_dev = MAVClass()  # TODO move this out of global context, bad practice
