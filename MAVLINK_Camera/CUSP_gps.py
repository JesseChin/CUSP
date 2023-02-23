#!/usr/bin/env python3

"""
Module for returning GPS coords
"""


from pymavlink import mavutil

import time
import sys


class GPS_data:
    X: float = 0
    Y: float = 0
    Z: float = 0


class GPSClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GPSClass, cls).__new__(cls)
        return cls.instance


def get_GPS() -> GPS_data:
    return


def fetch_GPS_data():
    """
    Send MAVLink command to FC to get GPS data,
    place data in GPS_data
    """
    return


def get_GPS_data():
    """
    Return GPS data without polling flight controller
    """
    latitude: float = 0
    longitude: float = 0
    altitude: int = 0
    return latitude, longitude, altitude


def GPS_init():
    return
