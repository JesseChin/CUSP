#!/usr/bin/env python3

from pymavlink import mavutil
from dataclasses import dataclass
import time
import sys

"""
Module for returning GPS coords
"""


class GPSClass:
    Latitude: float = 0  # rational64u
    LatitudeRef: str = "N"
    Longitude: float = 0  # rational64u
    LongitudeRef: str = "E"
    Altitude: float = 0  # rational64u
    Satellites: str = ""

    def set_mock_gps_data(self, latitude, longitude, altitude):
        self.Latitude = latitude
        self.Longitude = longitude
        self.Altitude = altitude

    def get_GPS_data(self):
        return self.Latitude, self.Longitude, self.Altitude

    def fetch_GPS_data(self):
        """
        Send MAVLink command to FC to get GPS data,
        place data in GPS_data

        retVal: Error code
        """
        return


GPS_dev = GPSClass()
