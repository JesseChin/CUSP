from pymavlink import mavutil

if __name__ == "__main__":
    connection = mavutil.mavlink_connection('/dev/serial0', baud=57600)
    
    connection.wait_heartbeat()
    
    connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_CAMERA, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    
    while(True):
        msg = the_connection.recv_match(blocking=True)
        
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
            if mavutil.all_printable(msg.data):
                sys.stdout.write(msg.data)
                sys.stdout.flush()
        else:
        
            if msg.get_type() == "MAV_CMD_REQUEST_MSG" and msg.param1 == 259 :
                command_ack_send() #need params
                camera_information_send()
            
            
                
            #Message is valid
            # Use the attribute
            print('Mode: %s' % msg.mode)