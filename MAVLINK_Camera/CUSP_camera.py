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
import subprocess


def device_exists(path):
    try:
        return stat.S_ISBLK(os.stat(path).st_mode)
    except:
        return False


picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()
# picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})


def capture_rgb():
    """
    Capture RGB image, return error status
    """
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

    metadata = picam2.switch_mode_and_capture_file(
        camera_config, OUTPUT_PATH + filename
    )
    print(metadata, imx477)

    if write_metadata(OUTPUT_PATH + filename, imx477) == Error.NO_ERROR:
        return Error.NO_ERROR

    return Error.CAPTURE_ERROR


def capture_thermal():
    """
    Capture thermal image, return error status if error, else return path
    """
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

    try:
        cmd = "sudo chown sixth:sixth " + OUTPUT_PATH + filename + "000000.gray"
        os.system(cmd)
        # TODO convert to be usable by user
        # TODO use tmpfs
        convert_raw(
            OUTPUT_PATH + filename + "000000.gray",
            OUTPUT_PATH + filename,
            "TIFF",
            (120, 160),
        )
    except:
        return Error.CAMERA_MISSING
    if write_metadata(OUTPUT_PATH + filename, flir_lepton_3_5) == Error.NO_ERROR:
        return Error.NO_ERROR

    # return Error.CAPTURE_ERROR
    return Error.NO_ERROR


def capture_rgb_path(filepath: str):
    """
    Capture RGB image given path
    """
    camera_metadata = picam2.switch_mode_and_capture_file(camera_config, filepath)
    print(camera_metadata)

    if write_metadata(filepath, imx477) == Error.NO_ERROR:
        return Error.NO_ERROR

    return Error.CAPTURE_ERROR


def capture_thermal_path(filepath: str):
    """
    Capture thermal image given path
    """
    """LEPTON_DATA_COLLECTOR_PATH = (
        "sudo $HOME/CUSP/external/lepton_data_collector/lepton_data_collector"
    )
    OUTPUT_PATH = "/home/sixth/images/"
    """
    cmd = "lepton_data_collector -3 -c 1 -o " + filepath

    retcode = subprocess.call(cmd, shell=True)
    if os.path.exists(filepath + "000000.gray") == True:
        cmd = "sudo chown sixth:sixth " + filepath + "000000.gray"
        retcode = subprocess.call(cmd, shell=True)
        # TODO convert to be usable by user
        # TODO use tmpfs
        convert_raw(filepath + "000000.gray", filepath + ".tiff", "TIFF", (120, 160))
    else:
        return Error.CAMERA_MISSING
    try:
        if write_metadata(filepath + ".tiff", flir_lepton_3_5) == Error.NO_ERROR:
            return Error.NO_ERROR
    except:

        # return Error.CAPTURE_ERROR
        return Error.NO_ERROR


def write_metadata(filename: str, camera_type: dict):
    latitude, longitude, _ = GPS_dev.get_GPS_data()
    with ExifToolHelper() as et:
        et.set_tags(
            [filename],
            tags={
                "GPSLatitude": latitude,
                "GPSLatitudeRef": "N" if latitude >= 0 else "S",
                "GPSLongitude": longitude,
                "GPSLongitudeRef": "E" if longitude >= 0 else "W",
                "GPSAltitude": GPS_dev.Altitude * 1e-3,
                "GPSAltitudeRef": 0 if GPS_dev.Altitude >= 0 else -1,
                "GPSSpeed": GPS_dev.vel * 0.036,
                "GPSSpeedRef": "K",
                "GPSImgDirection": GPS_dev.yaw * (180 / math.pi),
                "GPSImgDirectionRef": "T",
                "GPSTimeStamp": GPS_dev.time_usec,
                "GPSSatellites": GPS_dev.satellites_visible,
                "GPSProcessingMethod": "GPS",
                "FocalLength": camera_type["FocalLength"],
                "FocalPlaneXResolution": camera_type["SensorWidth"],
                "FocalPlaneYResolution": camera_type["SensorHeight"],
                "FocalPlaneResolutionUnit": 5,  # Corresponds to um
            },
            params=["-P", "-overwrite_original"],
        )
    return Error.NO_ERROR


# TODO Set up tmpfs for capturing Lepton RAWs
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
