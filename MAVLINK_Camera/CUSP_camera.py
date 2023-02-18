#!/usr/bin/env python3

import exiftool
from CUSP_error_types import Error
import os
from datetime import datetime
import stat

def device_exists(path):
     try:
             return stat.S_ISBLK(os.stat(path).st_mode)
     except:
             return False

def capture_rgb():
    # Check for presence of camera
    # check ls /dev/video1
    if device_exists("/dev/video1") == False:
        return Error.CAMERA_MISSING

    # Set file name
    dt = datetime.now()
    filename = (str)dt
    # Capture image
    OUTPUT_PATH = '/home/sixth/images/'
    cmd = 'libcamera-still -t 5000 -o ' + OUTPUT_PATH + filename

    os.system(cmd)

    if write_metadata(OUTPUT_PATH + filename) == Error.NO_ERROR:
        return Error.NO_ERROR


def capture_thermal():
    # Check for presence of camera
    # check ls /dev/video0, if nothing return an error
    if device_exists("/dev/video0") == False:
        return Error.CAMERA_MISSING

    # Set file name
    dt = datetime.now()
    filename = (str)dt
    # Capture image

    LEPTON_DATA_COLLECTOR_PATH = 'external/lepton_data_collector/lepton_data_collector'
    OUTPUT_PATH = '/home/sixth/images/'
    cmd = LEPTON_DATA_COLLECTOR_PATH + ' -3 -c 1 -o' + OUTPUT_PATH + filename

    os.system(cmd)

    if write_metadata(OUTPUT_PATH + filename) == Error.NO_ERROR:
        return Error.NO_ERROR


def write_metadata(filename):
    return Error.NO_ERROR
