#!/usr/bin/env python3
"""
Capturing modes for CUSP
Currently working on: PWM and Overlap
MAVLink Camera Protocol not supported yet
"""

from CUSP_camera import *
from math import sin, cos, tan, asin, acos, atan

# import RPi.GPIO as GPIO
# Use apigpio instead as it has asyncio support
from time import sleep
from threading import Thread, Lock
from datetime import datetime


class Trigger_Timer:
    """
    When activated,
    """

    periodSeconds = 5
    active = False
    triggerMutex = Lock()

    def set_period(self, seconds):
        self.periodSeconds = seconds

    def set_frequency(self, Hz):
        self.periodSeconds = 1 / Hz

    def trigger_loop(self):
        with self.triggerMutex:
            if self.active:
                startTime = time.time()
                capture_rgb()
                capture_thermal()

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
    fov = 34.2 # vertical lepton FOV
    alt_start = 0
    overlap_percent = 25

    def set_GPS(self, gpsObject):
        self.gpsObject = gpsObject

    def set_fov(self, fov):
        self.fov = fov

    def set_stating_altitude(self, alt_start):
        self.alt_start = alt_start

    def set_overlap_percent(self, overlap_percent):
        self.overlap_percent = overlap_percent

    def trigger_loop(self):
                
        lat_prev, long_prev, alt_prev = 0,0,0

        with self.triggerMutex:
            if self.active:
                
                lat_now, long_now, alt_now = self.gpsObject.get_GPS_data()

                distance_m = acos(sin(lat_prev)*sin(long_prev)+cos(lat_prev)*cos(long_prev)*cos(long_now-long_prev))*6371*1000

                if distance_m > ((100-self.overlap_percent)/100.0)*2*(alt_now-self.alt_start)*tan(self.fov/2):
                    lat_prev, long_prev, alt_prev = lat_now, long_now, alt_now
                    capture_rgb()
                    capture_thermal()
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
