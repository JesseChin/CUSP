#!/usr/bin/env python3

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
import queue
import grpc
import os, sys

sys.path.append(
    os.path.join(os.path.dirname(__file__), "../rt-flight/raspberry_pi_code/protos")
)
import messaging_pb2
import messaging_pb2_grpc

"""
Main program to run CUSP
Handles all MAVLink communication here
"""

LEPTON_HFOV = 45.6
LEPTON_VFOV = 34.2

msg_buffer = queue.Queue()


def poll_GPS(periodSeconds, GPS, the_connection):
    # Handle polling GPS data here

    # Initial GPS run for setting home altitude
    the_connection.wait_gps_fix()

    while True:
        msg = the_connection.recv_match(type="GPS_RAW_INT", blocking=True)
        GPS.set_GPS_data_RAW_INT(msg)

        msg = the_connection.recv_match(type="ATTITUDE", blocking=True)
        GPS.set_GPS_data_ATTITUDE(msg)

        msg = the_connection.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
        GPS.set_GPS_rel_height(msg)

        # might have to bump up frequency depending on how fast it's flying
        sleep(periodSeconds)


def process_path_buffer(msg_buffer, the_connection):
    channel = grpc.insecure_channel("localhost:50951")
    stub = messaging_pb2_grpc.MessagingServiceStub(channel)
    while True:
        item = msg_buffer.get(block=True)
        # Write item to GRPC so that the model can see
        # Print path sending as a test
        print("Sending path: ", item)
        response = stub.GetBoundingBoxes(messaging_pb2.File_Payload(path=item))
        print("Sending to GCS: ", response.bboxes)
        # print(response.status)
        the_connection.mav.statustext_send(
            mavutil.mavlink.MAV_SEVERITY_NOTICE, str(response.bboxes).encode()
        )
        sleep(1)


def startTrigger(trigger):
    while True:
        trigger.trigger_loop()


def main():

    # Activate connection to flight controller

    master = mavutil.mavlink_connection(
        "udp:127.0.0.1:14550", baud=57600, source_system=1, source_component=2
    )
    print("Creating connection...")

    master.wait_heartbeat()
    print(
        "Heartbeat from system (system %u component %u)"
        % (master.target_system, master.target_component)
    )

    GPSprocess = Thread(target=poll_GPS, args=(0.1, GPS_dev, master,),)
    GPSprocess.start()

    configJSON = open("../Web_App/form_data.json")
    configData = json.load(configJSON)
    configData = json.loads(configData)
    oldData = configData

    trigger = Trigger_Timer(msg_buffer)
    trigger.deactivate_trigger()
    triggerProcess = Thread(target=startTrigger, args=(trigger,))
    triggerProcess.start()

    trigger.set_period(15)

    ModelSenderProcess = Thread(target=process_path_buffer, args=(msg_buffer, master,))
    ModelSenderProcess.start()

    # Wait until GPS receives data
    # while any(v is None for v in GPS_dev.get_GPS_data()):
    while GPS_dev.get_GPS_data() is None:
        print("Waiting for GPS uplink")
        sleep(1)

    lat_start, long_start, alt_start = GPS_dev.get_GPS_data()

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
                    trigger = Trigger_Timer()
                    trigger.set_period(15)
                elif configData["acmode"] == "Overlap":
                    trigger = Trigger_Overlap()
                    trigger.set_fov(LEPTON_VFOV)
                    trigger.set_stating_altitude(alt_start)
                    trigger.set_overlap_percent(configData["along-track_overlap"])
                # elif (configData['acmode'] == "PWM"):
                #     trigger = Trigger_PWM()
            altitude_target = configData["target_altitude"]
            altitude_tolerance = configData["target_altitude_tolerance"]

        latitude, longitude, altitude = GPS_dev.get_GPS_data()

        if float(altitude_target) > altitude - float(altitude_tolerance) and float(
            altitude_target
        ) < altitude + float(altitude_tolerance):
            trigger.activate_trigger()
            print(f"Altitude within tolerance: {altitude}")
        else:
            trigger.deactivate_trigger()
            print(f"Altitude outside tolerance: {altitude}")

        sleep(1)
        tick += 1


if __name__ == "__main__":
    main()
