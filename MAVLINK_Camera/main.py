#!/usr/bin/env python3

import asyncio
from typing_extensions import get_args
from pymavlink import mavutil
import time
import sys
from CUSP_camera import *
from CUSP_trigger import *
from CUSP_gps import *
import json
import random

# from multiprocessing import Process
from threading import Thread, Lock

"""
Main program to run CUSP
Handles all MAVLink communication here
"""


def poll_GPS(periodSeconds, GPS, the_connection):
    # Handle polling GPS data here

    # Initial GPS run for setting home altitude
    the_connection.wait_gps_fix()
    # msg = the_connection.recv_match(type="GPS_RAW_INT", blocking=True)

    while True:
        # GPS_dev.fetch_GPS_data()

        msg = the_connection.recv_match(type="GPS_RAW_INT", blocking=True)
        GPS.set_GPS_data_RAW_INT(msg)

        msg = the_connection.recv_match(type="ATTITUDE", blocking=True)
        GPS.set_GPS_data_ATTITUDE(msg)

        msg = the_connection.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
        GPS.set_GPS_rel_height(msg)

        # might have to bump up frequency depending on how fast it's flying
        sleep(periodSeconds)


def startTrigger(trigger):
    while True:
        trigger.trigger_loop()


def main():

    # Activate connection to flight controller

    # master = mavutil.mavlink_connection( "tcp:127.0.0.1:5760", baud=57600, source_system=1, source_component=2)
    master = mavutil.mavlink_connection(
        "udp:127.0.0.1:14550", baud=57600, source_system=1, source_component=2
    )
    # master = mavutil.mavlink_connection('udp:10.136.27.15:14550', baud=57600, source_system=1, source_component=2)
    print("Creating connection...")

    master.wait_heartbeat()
    print(
        "Heartbeat from system (system %u component %u)"
        % (master.target_system, master.target_component)
    )

    """
    # Initialize callback for PWM triggering
    PWM_init()
    Overlap_init()

    GPS_init()
    """

    # GPS_dev = GPSClass()

    GPSprocess = Thread(target=poll_GPS, args=(0.1, GPS_dev, master,),)
    GPSprocess.start()

    configJSON = open("../Web_App/form_data.json")
    configData = json.load(configJSON)
    configData = json.loads(configData)
    oldData = configData

    trigger = Trigger_Timer()
    trigger.deactivate_trigger()
    triggerProcess = Thread(target=startTrigger, args=(trigger,))
    triggerProcess.start()

    trigger.set_period(15)

    # Wait until GPS receives data
    # while any(v is None for v in GPS_dev.get_GPS_data()):
    while GPS_dev.get_GPS_data() is None:
        print("Waiting for GPS uplink")
        sleep(1)

    tick = 0
    while True:
        if tick % 10 == 0:
            print("JSON verified")
            configJSON = open("../Web_App/form_data.json")
            oldData = configData
            configData = json.load(configJSON)
            configData = json.loads(configData)
            if oldData["acmode"] != configData["acmode"]:
                # update trigger mode
                if configData["acmode"] == "Periodic":
                    trigger = Trigger_Timer()  # TODO add mutex to the startTrigger loop
                    trigger.set_period(15)
                # elif (configData['acmode'] == "Overlap"):
                #     trigger = Trigger_Overlap()
                # elif (configData['acmode'] == "PWM"):
                #     trigger = Trigger_PWM()

        latitude, longitude, altitude = GPS_dev.get_GPS_data()

        if float(configData["target_altitude"]) > altitude - float(
            configData["target_altitude_tolerance"]
        ) and float(configData["target_altitude"]) < altitude + float(
            configData["target_altitude_tolerance"]
        ):
            trigger.activate_trigger()
            print(f"Altitude within tolerance: {altitude}")
        else:
            trigger.deactivate_trigger()
            print(f"Altitude outside tolerance: {altitude}")

        sleep(1)
        tick += 1


if __name__ == "__main__":
    main()
