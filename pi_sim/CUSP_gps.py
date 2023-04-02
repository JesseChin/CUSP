#!/usr/bin/env python3

"""
Module for returning GPS coords
"""


from pymavlink import mavutil
import time
import sys
import board
import busio
import adafruit_gps
from threading import Thread, Lock

"""
Module for returning GPS coords
"""


class GPSClass:

    GPSmutex = Lock()

    def __init__(self) -> None:
        self.Latitude: float = 0  # rational64u
        self.LatitudeRef: str = "N"
        self.Longitude: float = 0  # rational64u
        self.LongitudeRef: str = "E"
        self.Altitude: float = 0  # rational64u
        self.Satellites: str = ""

        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.gps = adafruit_gps.GPS_GtopI2C(self.i2c)  # Use I2C interface
        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Set update rate to 4Hz
        self.gps.send_command(b"PMTK220,250")

    def set_mock_gps_data(self, latitude, longitude, altitude):
        """
        For manually mocking coordinates
        """
        with self.GPSmutex:
            self.Latitude = latitude
            self.Longitude = longitude
            self.Altitude = altitude

    def get_GPS_data(self):
        with self.GPSmutex:
            return self.Latitude, self.Longitude, self.Altitude

    def fetch_GPS_data(self):
        """
        Send MAVLink command to FC to get GPS data,
        place data in GPS_data

        retVal: Error code
        """
        self.gps.update()
        if not self.gps.has_fix:
            print("Waiting for fix...")
            return

        print(
            "Precise Latitude: {:2.}{:2.4f} degrees".format(
                self.gps.latitude_degrees, self.gps.latitude_minutes
            )
        )
        print(
            "Precise Longitude: {:2.}{:2.4f} degrees".format(
                self.gps.longitude_degrees, self.gps.longitude_minutes
            )
        )
        self.Latitude = self.gps.latitude
        self.Longitude = self.gps.longitude
        self.Altitude = self.gps.altitude_m
        return


GPS_dev = GPSClass()  # TODO move this out of global context, bad practice
