#!/usr/bin/env python3

from enum import Enum


class Error(Enum):
    NO_ERROR = 0
    CAPTURE_ERROR = 1
    NO_GPS = 2
    GPS_READ_ERROR = 3
    CAMERA_MISSING = 4

class UnknownCaptureError(Exception):
    """Unknown error while capturing"""
    
class NoGPSStatus(Exception):
    """No GPS detected"""
    
class CameraMissing(Exception):
    """Camera not detected, perhaps a wiring fault"""