#!/usr/bin/env python3
# Unused, remove soon


import time
from pymavlink import mavutil


def request_message_interval(
    message_id: int, frequency_hz: float, master: mavutil.mavlink_connection
):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        message_id,  # The MAVLink message ID
        1e6
        / frequency_hz,  # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0,
        0,
        0,
        0,  # Unused parameters
        0,  # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )
