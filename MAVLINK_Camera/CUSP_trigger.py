#!/usr/bin/env python3
"""
Capturing modes for CUSP
Currently working on: PWM and Overlap
MAVLink Camera Protocol not supported yet
"""


# import RPi.GPIO as GPIO
# Use apigpio instead as it has asyncio support
from time import sleep


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
