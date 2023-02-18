#!/usr/bin/env python3
"""
Mocked functions for triggering modes
DO NOT call any actual hardware here! Any calls to hardware should be replaced with
returns to Error.NO_ERROR

We are assuming hardware calls works for these functions.
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
