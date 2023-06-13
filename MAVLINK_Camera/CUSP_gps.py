#!/usr/bin/env python3

from dataclasses import dataclass
import time
import sys
from enum import Enum

# from multiprocessing import Process, Lock
from threading import Thread, Lock

"""
Module for returning GPS coords
"""

class GPS_FIX_TYPE(Enum):
    GPS_FIX_TYPE_NO_GPS = 0
    GPS_FIX_TYPE_NO_FIX = 1
    GPS_FIX_TYPE_2D_FIX = 2
    GPS_FIX_TYPE_3D_FIX = 3
    GPS_FIX_TYPE_DGPS = 4
    GPS_FIX_TYPE_RTK_FLOAT = 5
    GPS_FIX_TYPE_RTK_FIXED = 6
    GPS_FIX_TYPE_STATIC = 7
    GPS_FIX_TYPE_PPP = 8

@dataclass
class GPSClass:

    GPSmutex = Lock()

    time_usec: int  # Timestamp in UNIX Epoch
    fix_type: int  # GPS fix type
    # Latitude and Longitude is in degE7. To convert, divide by 1.0e7
    Latitude: int  # Latitude  (WGS84, EGM96 ellipsoid)
    Longitude: int  # Longitude (WGS84, EGM96 ellipsoid)
    # Altitude in mm
    Altitude: int  # Altitude (Mean Sea Level)
    eph: int  # GPS HDOP horizontal dilution of position (unitless*100)
    epv: int  # GPS VDOP vertical dilution of position (unitless*100)
    # Velocity is in cm/s
    vel: int  # GPS ground speed
    # Course over Ground in cdeg
    # Course over ground (NOT heading, but direction of movement) in degrees * 100, 0.0..359.99degrees
    cog: int
    satellites_visible: int  # Number of satellites visible
    # After this line is part of MAVLink 2 extension fields
    # alt_ellipsoid, h_acc, v_acc, vel_acc units are in mm and mm/s
    # Altitude (above WGS84, EGM96 ellipsoid) Positive for up
    alt_ellipsoid: int
    h_acc: int  # Position uncertainty
    v_acc: int  # Altitude uncertainty
    vel_acc: int  # Speed uncertainty
    # hdg_acc is in degE5
    hdg_acc: int  # Heading / track uncertainty
    # yaw in cdeg
    # Yaw in earth frame from north. Set to 0 if GPS does not provide yaw.
    yaw_gps: int

    # All units are in rad or rad/s
    roll: float
    pitch: float
    yaw: float
    pitchspeed: float
    yawspeed: float

    initial_latitude: int
    initial_longitude: int
    initial_altitude: int

    rel_altitude: float
    
    def __init__(self):
        self.time_usec = None
        self.fix_type = None
        self.Latitude = None
        self.Longitude = None
        self.Altitude = None
        self.eph = None
        self.epv = None
        self.vel = None
        self.cog = None
        self.satellites_visible = None
        self.alt_ellipsoid = None
        self.h_acc = None
        self.v_acc = None
        self.vel_acc = None
        self.hdg_acc = None
        self.yaw_gps = None

    def set_mock_gps_data(self, latitude, longitude, altitude):
        with self.GPSmutex:
            self.Latitude = latitude
            self.Longitude = longitude
            self.Altitude = altitude

    def get_GPS_data(self):
        with self.GPSmutex:
            if self.Latitude is None:
                return None
            lat = self.Latitude * 1.0e-7
            lng = self.Longitude * 1.0e-7
            alt = self.rel_altitude * 1e-3
            return lat, lng, alt

    def fetch_GPS_data(self):
        """
        Manually send MAVLink command to FC to get GPS data,
        place data in GPS_data

        Unused at the current moment as we cannot guarentee timing requirements

        retVal: Error code
        """

    def set_GPS_data_AHRS2(self, msg):
        """
        Set the GPS data using the AHRS2 msg pulled from MAVLink
        """

    def set_GPS_data_RAW_INT(self, msg):
        """
        Set the GPS data by receiving a GPS_RAW_INT message via MAVLink
        and parsing it
        """
        self.time_usec = msg.time_usec
        self.fix_type = msg.fix_type
        self.Latitude = msg.lat
        self.Longitude = msg.lon
        self.Altitude = msg.alt
        self.eph = msg.eph
        self.epv = msg.epv
        self.vel = msg.vel
        self.cog = msg.cog
        self.satellites_visible = msg.satellites_visible
        self.alt_ellipsoid = msg.alt_ellipsoid
        self.h_acc = msg.h_acc
        self.v_acc = msg.v_acc
        self.vel_acc = msg.vel_acc
        self.hdg_acc = msg.hdg_acc
        self.yaw_gps = msg.yaw

    def set_GPS_data_ATTITUDE(self, msg):
        """
        Sets the attitude based on the ATTITUDE message in MAVLink
        Required for writing the compass for our metadata
        """
        self.roll = msg.roll
        self.pitch = msg.pitch
        self.yaw = msg.yaw
        self.rollspeed = msg.rollspeed
        self.pitchspeed = msg.pitchspeed
        self.yawspeed = msg.yawspeed

    def set_GPS_rel_height(self, msg):
        """
        """
        self.rel_altitude = msg.relative_alt