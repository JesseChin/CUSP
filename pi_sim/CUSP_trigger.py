#!/usr/bin/env python3
"""
Capturing modes for CUSP
Currently working on: PWM and Overlap
MAVLink Camera Protocol not supported yet
"""

from CUSP_camera import *

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

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def Overlap_init():
    """
    Set up Overlap triggering mode
    """
    return
