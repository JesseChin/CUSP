import time
from pymavlink import mavutil
import sys

if __name__ == "__main__":

    # Create the connection
    # master = mavutil.mavlink_connection('tcp:127.0.0.1:5760')
    master = mavutil.mavlink_connection('udp:127.0.0.1:14550', source_system=1, source_component=2)
    # Wait a heartbeat before sending commands
    print("Creating connection...")
    master.wait_heartbeat()

    print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))
    # Request parameter
    '''
    master.mav.param_request_read_send(
        master.target_system, master.target_component,
        b'GPS_POS1_X',
        -1
    )
    '''
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        127, 10000000, 0, 0, 0, 0, 1)

    print('reading')
    # Print old parameter value
    message = master.recv_match(type='PARAM_VALUE', blocking=False).to_dict()
    print('name: %s\tvalue: %d' %
          (message['param_id'].decode("utf-8"), message['param_value']))

