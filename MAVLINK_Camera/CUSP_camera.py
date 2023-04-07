#!/usr/bin/env python3

import exiftool
from CUSP_error_types import Error
from camera_definitions import *
import os
from datetime import datetime
import stat
from exiftool import ExifToolHelper
from CUSP_gps import *
from picamera2 import Picamera2
from PIL import Image
import numpy as np
import math


def device_exists(path):
    try:
        return stat.S_ISBLK(os.stat(path).st_mode)
    except:
        return False


picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (imx477["SensorWidth"], imx477["SensorHeight"])}
)
picam2.configure(camera_config)
picam2.start()


def capture_rgb():
    # Check for presence of camera
    # check ls /dev/video1
    """
    if device_exists("/dev/video1") == False:
        return Error.CAMERA_MISSING
    """

    # Set file name
    dt = datetime.now()
    filename = dt.strftime("%Y-%m-%d_%H-%M-%S") + "_RGB.jpg"
    # Capture image
    OUTPUT_PATH = "/home/sixth/images/"
    metadata = picam2.capture_file(OUTPUT_PATH + filename)
    print(metadata, imx477)

    if write_metadata(OUTPUT_PATH + filename, imx477) == Error.NO_ERROR:
        return Error.NO_ERROR

    return Error.CAPTURE_ERROR


def capture_thermal():
    # Check for presence of camera
    # check ls /dev/video0, if nothing return an error
    """
    if device_exists("/dev/video0") == False:
        return Error.CAMERA_MISSING
    """

    # Set file name
    dt = datetime.now()
    filename = dt.strftime("%Y-%m-%d_%H-%M-%S") + "_IR"
    # Capture image

    # Currently saving as RAW in the beta build
    LEPTON_DATA_COLLECTOR_PATH = (
        "sudo $HOME/CUSP/external/lepton_data_collector/lepton_data_collector"
    )
    OUTPUT_PATH = "/home/sixth/images/"
    cmd = LEPTON_DATA_COLLECTOR_PATH + " -3 -c 1 -o" + OUTPUT_PATH + filename

    os.system(cmd)
    cmd = "sudo chown sixth:sixth " + OUTPUT_PATH + filename + "000000.gray"
    os.system(cmd)

    # TODO convert to be usable by user
    # TODO use tmpfs
    convert_raw(
        OUTPUT_PATH + filename + "000000.gray",
        OUTPUT_PATH + filename,
        "TIFF",
        (160, 120),
    )
    if write_metadata(OUTPUT_PATH + filename, flir_lepton_3_5) == Error.NO_ERROR:
        return Error.NO_ERROR

    # return Error.CAPTURE_ERROR
    return Error.NO_ERROR


def write_metadata(filename: str, camera_type: dict):
    latitude, longitude, altitude = GPS_dev.get_GPS_data()
    with ExifToolHelper() as et:
        et.set_tags(
            [filename],
            tags={
                "GPSLatitude": latitude,
                "GPSLatitudeRef": "N" if latitude <= 0 else "S",
                "GPSLongitude": longitude,
                "GPSLongitudeRef": "E" if longitude <= 0 else "W",
                "GPSAltitude": altitude,
                "GPSImgDirection": GPS_dev.yaw * (180 / math.pi),
                "GPSImgDirection": "T",
                "GPSTimeStamp": GPS_dev.time_usec,
                "GPSSatellites": GPS_dev.satellites_visible,
                "FocalLength": camera_type["FocalLength"],
                "FocalPlaneXResolution": camera_type["SensorWidth"],
                "FocalPlaneYResolution": camera_type["SensorHeight"],
                "FocalPlaneResolutionUnit": 5,  # Corresponds to um
            },
            params=["-P", "-overwrite_original"],
        )
    return Error.NO_ERROR


# TODO for myself; Set up tmpfs for capturing Lepton RAWs
def convert_raw(input_path: str, output_path: str, filetype: str, image_size: tuple):
    with open(input_path, "rb") as f:
        raw_data = np.fromfile(f, dtype=">u2")

    image_array = raw_data.reshape(image_size)

    # Minmax scaling
    min = np.min(image_array)
    max = np.max(image_array)
    image_norm = (65535 * ((image_array - min) / (max - min))).astype(np.uint16)

    image = Image.fromarray(image_norm)

    image.save(output_path, filetype)
