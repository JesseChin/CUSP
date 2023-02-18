from pymavlink import mavutil

import time
import sys

if __name__ == "__main__":
    
    the_connection = mavutil.mavlink_connection('tcp:127.0.0.1:5760', baud=57600, source_system=1, source_component=2)
    # the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14550', baud=57600, source_system=1, source_component=2)
    print("Creating connection...")
    
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    
    the_connection.mav.param_request_list_send(
        the_connection.target_system, the_connection.target_component
    )

while True:
    time.sleep(0.01)
    try:
        message = the_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'],
                                       message['param_value']))
    except Exception as error:
        print(error)
        sys.exit(0)
