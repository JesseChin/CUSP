from pymavlink import mavutil
import time
import sys

if __name__ == "__main__":
    
    the_connection = mavutil.mavlink_connection('/dev/ttyAMA0', baud=57600, source_system=1, source_component=2)
    print("Creating connection...")
    
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    
    '''
    the_connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_CAMERA, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    
    the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, opts.rate, 1)
    
    '''
    the_connection.mav.param_request_list_send(
        the_connection.target_system, the_connection.target_component
    )
    # time.sleep(1)
    '''
    try:
        altitude = the_connection.messages['GPS_RAW_INT'].alt
        timestamp = the_connection.time_since('GPS_RAW_INT')
        print("Altitude is " + str(altitude))
        print("Time is " + str(timestamp))
        
    except:
       print('No GPS_RAW_INT message received')

'''
while True:
    time.sleep(0.01)
    try:
        message = the_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'],
                                       message['param_value']))
    except Exception as error:
        print(error)
        sys.exit(0)