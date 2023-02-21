#!/usr/bin/env python3

from CUSP_error_types import Error
from exiftool import ExifToolHelper
from mock_gps import *


GPS = GPSClass()


def set_mock_metadata(latitude, longitude, altitude):
    GPS.set_mock_gps_data(latitude, longitude, altitude)
    return


filename = ""


def set_mock_filename(name):
    filename = name
    return


def capture_rgb():
    # Check for presence of camera

    # Capture image

    if write_metadata(filename) == Error.NO_ERROR:
        return Error.NO_ERROR


def capture_thermal():
    # Check for presence of camera

    # Capture image

    if write_metadata(filename) == Error.NO_ERROR:
        return Error.NO_ERROR


def write_metadata(filename):
    latitude, longitude, altitude = GPS.get_GPS_data()
    with ExifToolHelper() as et:
        et.set_tags(
            [filename],
            tags={
                "GPSLatitude": latitude,
                "GPSLongitude": longitude,
                "GPSAltitude": altitude,
            },
            params=["-P", "-overwrite_original"],
        )
    return Error.NO_ERROR
