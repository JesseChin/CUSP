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
import random
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
    mock_altitude: float = 28.0

    while True:
        # GPS_dev.fetch_GPS_data()
        mock_latitude += 0.03*random.random()
        mock_altitude += 0.01*random.random()

        GPS.set_mock_gps_data(mock_latitude, mock_longitude, mock_altitude)

        # might have to bump up frequency depending on how fast it's flying
        sleep(periodSeconds)

def startTrigger(trigger):
    while True:
        trigger.trigger_loop()

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
    configData = json.loads(configData)
    oldData = configData

    trigger = Trigger_Timer()
    trigger.deactivate_trigger()
    triggerProcess = Thread(target=startTrigger, args=(trigger,))
    triggerProcess.start()

    trigger.set_period(15)

    tick = 0
    while True:
        if tick%120 == 0:
            print("JSON verified")
            configJSON = open("../Web_App/form_data.json")
            oldData = configData
            configData = json.load(configJSON)
            configData = json.loads(configData)
            if (oldData['acmode'] != configData['acmode']):
                # update trigger mode
                if (configData['acmode'] == "Periodic"):
                    trigger = Trigger_Timer() # TODO add mutex to the startTrigger loop
                    trigger.set_period(15)
                # elif (configData['acmode'] == "Overlap"):
                #     trigger = Trigger_Overlap()
                # elif (configData['acmode'] == "PWM"):
                #     trigger = Trigger_PWM()
        
        latitude, longitude, altitude = GPS_dev.get_GPS_data()

        if (float(configData['target_altitude']) > altitude - float(configData['target_altitude_tolerance']) and float(configData['target_altitude']) < altitude + float(configData['target_altitude_tolerance'])):
            trigger.activate_trigger()
            print(f"Altitude within tolerance: {altitude}")
        else:
            trigger.deactivate_trigger()
            print(f"Altitude outside tolerance: {altitude}")

        sleep(1)
        tick += 1


if __name__ == "__main__":
    main()
