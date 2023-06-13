#!/usr/bin/env python3

from CUSP_error_types import Error
from camera_definitions import flir_lepton_3_5
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
from typing import Tuple
from multiprocessing import Lock
import cv2
from params import *


def device_exists(path):
    try:
        return stat.S_ISBLK(os.stat(path).st_mode)
    except:
        return False


class RGBCamera:
    def __init__(self, cameraDef):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration(
            main={
                "format": "RGB888",
                "size": (cameraDef["XResolution"], cameraDef["YResolution"]),
            }
        )
        self.picam2.configure(camera_config)
        self.picam2.start()
        self._lock = Lock()
        self._cameraDef = cameraDef

    def capture(self, filename: str, GPS) -> Error:
        """
        Captures RGB image
        """
        with self._lock as l:
            status = self._capture_sync(filename, GPS)
        return status

    def _capture_sync(self, filename:str, GPS) -> Error:
        """
        Synchronous blocking version of capture
        """
        # Capture image
        RGB888 = self.picam2.capture_array("main")
        cv2.imwrite(filename, RGB888)

        if any(x is None for x in GPS):
            return Error.CAPTURE_ERROR
        if (
            write_metadata(OUTPUT_PATH + filename, self._cameraDef, GPS)
            == Error.NO_ERROR
        ):
            return Error.NO_ERROR

        return Error.CAPTURE_ERROR


class ThermalCamera:

# TODO Set up tmpfs for capturing Lepton RAWs
    def _convert_raw(self, input_path: str, output_path: str, filetype: str, image_size: tuple):
        with open(input_path, "rb") as f:
            raw_data = np.fromfile(f, dtype=">u2")

        image_array = raw_data.reshape(image_size)

        # Minmax scaling
        min = np.min(image_array)
        max = np.max(image_array)
        image_norm = (65535 * ((image_array - min) / (max - min))).astype(np.uint16)

        image = Image.fromarray(image_norm)

        image.save(output_path, filetype)
    def capture(self, filename, GPS):
        """
        Capture thermal image, return error status if error, else return path
        """

        # Currently saving as RAW in the beta build
        cmd = "sudo " + LEPTON_DATA_COLLECTOR_PATH + " -3 -c 1 -o" + OUTPUT_PATH + filename

        os.system(cmd)

        try:
            cmd = "sudo chown sixth:sixth " + OUTPUT_PATH + filename + "000000.gray"
            os.system(cmd)
            # TODO convert to be usable by user
            # TODO use tmpfs
            self._convert_raw(
                OUTPUT_PATH + filename + "000000.gray",
                OUTPUT_PATH + filename,
                "TIFF",
                (120, 160),
            )
        except:
            return Error.CAMERA_MISSING
        if (
            write_metadata(OUTPUT_PATH + filename, flir_lepton_3_5, GPS)
            == Error.NO_ERROR
        ):
            return Error.NO_ERROR

        return Error.NO_ERROR

def write_metadata(filename: str, camera_type: dict, GPS):
    with ExifToolHelper() as et:
        et.set_tags(
            [filename],
            tags={
                "GPSLatitude": GPS.latitude,
                "GPSLatitudeRef": "N" if GPS.latitude >= 0 else "S",
                "GPSLongitude": GPS.longitude,
                "GPSLongitudeRef": "E" if GPS.longitude >= 0 else "W",
                "GPSAltitude": GPS.Altitude * 1e-3,
                "GPSAltitudeRef": 0 if GPS.Altitude >= 0 else -1,
                "GPSSpeed": GPS.vel * 0.036,
                "GPSSpeedRef": "K",
                "GPSImgDirection": GPS.yaw * (180 / math.pi),
                "GPSImgDirectionRef": "T",
                "GPSTimeStamp": GPS.time_usec,
                "GPSSatellites": GPS.satellites_visible,
                "GPSProcessingMethod": "GPS",
                "FocalLength": camera_type["FocalLength"],
                "FocalPlaneXResolution": camera_type["SensorWidth"],
                "FocalPlaneYResolution": camera_type["SensorHeight"],
                "FocalPlaneResolutionUnit": 5,  # Corresponds to um
            },
            params=["-P", "-overwrite_original"],
        )
    return Error.NO_ERROR


