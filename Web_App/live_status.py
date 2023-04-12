from time import sleep
import pickle
import os
from CUSP_gps import *
import math

statvfs = os.statvfs(os.getcwd())


def storage():
    output = (
        str(round(statvfs.f_bavail * statvfs.f_frsize * 1e-9, 2))
        + " out of "
        + str(round(statvfs.f_blocks * statvfs.f_frsize * 1e-9, 2))
        + " GB"
    )
    return output


class GPS_Reader:
    def __init__(self):
        with open("../MAVLINK_Camera/gps.pkl", "rb") as f:
            self.GPS_Data = pickle.load(f)

    def GPS_update(self):
        with open("../MAVLINK_Camera/gps.pkl", "rb") as f:
            self.GPS_Data = pickle.load(f)

    def get_lat_long(self):
        lat, long, _ = self.GPS_Data.get_GPS_data()
        return lat, long

    def get_location(self):
        return self.GPS_Data.get_GPS_data()

    def get_connected(self):
        return (
            True
            if self.GPS_Data.fix_type is not GPS_FIX_TYPE.GPS_FIX_TYPE_NO_FIX
            or GPS_FIX_TYPE.GPS_FIX_TYPE_NO_GPS
            else False
        )

    def get_sattelites(self):
        return self.GPS_Data.satellites_visible

    def get_altitude(self):
        _, _, altitude = self.GPS_Data.get_GPS_data()
        return altitude

    def get_heading(self):
        return self.GPS_Data.yaw * (180 / math.pi)

    def get_speed(self):
        return self.GPS_Data.vel * 1e-2
