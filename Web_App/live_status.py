import os
statvfs = os.statvfs(os.getcwd())

def storage():
    output = str(round(statvfs.f_bavail * statvfs.f_frsize * 1e-9, 2)) + " out of " + str(round(statvfs.f_blocks * statvfs.f_frsize * 1e-9, 2)) + " GB"
    return output

def other():
    output = 5
    return output

def connected():
    output = True
    return output