#!/usr/bin/env python3

import exiftool
from CUSP_error_types import Error


def capture_rgb():
    # Check for presence of camera

    # Capture image

    if write_metadata() == Error.NO_ERROR:
        return Error.NO_ERROR


def capture_thermal():
    # Check for presence of camera

    # Capture image

    if write_metadata() == Error.NO_ERROR:
        return Error.NO_ERROR


def write_metadata():
    return Error.NO_ERROR
