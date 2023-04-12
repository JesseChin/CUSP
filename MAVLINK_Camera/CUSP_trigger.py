#!/usr/bin/env python3
"""
Capturing modes for CUSP
Currently working on: PWM and Overlap
MAVLink Camera Protocol not supported yet
"""

from CUSP_camera import *
from math import sin, cos, tan, asin, acos, atan, pi, atan2, sqrt

# import RPi.GPIO as GPIO
# Use apigpio instead as it has asyncio support
from time import sleep
from threading import Thread, Lock
from datetime import datetime

from multiprocessing import Process

import queue


class Trigger_Timer:
    """
    When activated, turn on trigger on each period
    """

    def __init__(self, msg_buffer, period=15):
        self.periodSeconds = period
        self.active = False
        self.triggerMutex = Lock()
        self.msg_buffer = msg_buffer

    def set_period(self, seconds):
        self.periodSeconds = seconds

    def set_frequency(self, Hz):
        self.periodSeconds = 1 / Hz

    def trigger_loop(self):
        with self.triggerMutex:
            if self.active:
                startTime = time.time()

                dt = datetime.now()
                filepath = "/home/sixth/images/" + dt.strftime("%Y-%m-%d_%H-%M-%S")
                print("Capturing RGB")
                retcode = capture_rgb_path(filepath + "_RGB.jpg")
                if retcode == Error.NO_ERROR:
                    self.msg_buffer.put(filepath + "_RGB.jpg")
                print("Capturing IR")
                retcode = capture_thermal_path(filepath + "_IR")
                if retcode == Error.NO_ERROR:
                    print("Adding IR path to buffer")
                    self.msg_buffer.put(filepath + "_IR.tiff")

                now = time.time()
                waitTime = self.periodSeconds - (now - startTime)
                print(
                    f"took {round(now - startTime,1)}s. waiting {round(waitTime,1)}s for next capture"
                )
                if waitTime < 0.1:
                    waitTime = 0.1
                sleep(waitTime - 0.1)
        sleep(0.1)

    def activate_trigger(self):
        with self.triggerMutex:
            self.active = True

    def deactivate_trigger(self):
        with self.triggerMutex:
            self.active = False


class Trigger_PWM:
    """
    Trigger capturing image upon receiving a HIGH PWM signal
    Implemented as a singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def PWM_callback():
    return


def PWM_init():
    """
    Set up PWM GPIO and inialize callback function
    """
    return


class Trigger_Overlap:
    """
    Trigger capturing image upon receiving a HIGH PWM signal
    Implemented as a singleton
    """

    active = False
    triggerMutex = Lock()

    gpsObject = None
    fov = 34.2  # vertical lepton FOV
    alt_start = 0
    overlap_percent = 25

    lat_prev, long_prev, alt_prev = 0, 0, 0

    def __init__(self, msg_buffer):
        self.active = False
        self.triggerMutex = Lock()
        self.msg_buffer = msg_buffer

    def set_GPS(self, gpsObject):
        self.gpsObject = gpsObject

    def set_fov(self, fov):
        self.fov = fov

    def set_stating_altitude(self, alt_start):
        self.alt_start = alt_start

    def set_overlap_percent(self, overlap_percent):
        self.overlap_percent = overlap_percent

    def trigger_loop(self):

        with self.triggerMutex:
            if self.active:

                lat_now, long_now, alt_now = self.gpsObject.get_GPS_data()

                R = 6371
                lat_prev_r = self.lat_prev * pi/180
                lat_now_r = lat_now * pi/180
                dLat = (lat_now-self.lat_prev) * pi/180
                dLong = (long_now-self.long_prev) * pi/180

                a = sin(dLat/2) * sin(dLat/2) + cos(lat_prev_r) * cos(lat_now_r) * sin(dLong/2) * sin(dLong/2)
                distance_m = R * 2 * atan2(sqrt(a), sqrt(1-a))

                print(f"Distance traveled: {distance_m}m")

                if distance_m > ((100 - self.overlap_percent) / 100.0) * 2 * (
                    alt_now - self.alt_start
                ) * tan(self.fov / 2):
                    self.lat_prev, self.long_prev, self.alt_prev = lat_now, long_now, alt_now
                    dt = datetime.now()
                    filepath = "/home/sixth/images/" + dt.strftime("%Y-%m-%d_%H-%M-%S")
                    print("Capturing RGB")
                    retcode = capture_rgb_path(filepath + "_RGB.jpg")
                    if retcode == Error.NO_ERROR:
                        self.msg_buffer.put(filepath + "_RGB.jpg")
                    print("Capturing IR")
                    retcode = capture_thermal_path(filepath + "_IR")
                    if retcode == Error.NO_ERROR:
                        print("Adding IR path to buffer")
                        self.msg_buffer.put(filepath + "_IR.tiff")
                else:
                    sleep(0.2)

    def activate_trigger(self):
        with self.triggerMutex:
            self.active = True

    def deactivate_trigger(self):
        with self.triggerMutex:
            self.active = False


def Overlap_init():
    """
    Set up Overlap triggering mode
    """
    return
