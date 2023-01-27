from pymavlink import mavutil
import time

STATE_INIT = 0
STATE_IDLE = 1
STATE_SEND = 2


if __name__ == "__main__":
    state = STATE_INIT
    
    connection = mavutil.mavlink_connection('/dev/ttyAMA0', baud=57600)
    print("Creating connection...")
    
    
    connection.wait_heartbeat()
    print("Heartbeat detected!")
    
    connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_CAMERA, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    
    while(True):
        if(state == STATE_INIT):
            
            #send a test message
            connection.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"Testing Message!!!".encode())
            
            msg = connection.recv_match(blocking=True)
        
            if not msg:
                pass
            if msg.get_type() == "BAD_DATA":
                if mavutil.all_printable(msg.data):
                    sys.stdout.write(msg.data)
                    sys.stdout.flush()
                else:
                    if msg.get_type() == "MAV_CMD_REQUEST_MSG" and msg.param1 == 259 :
                        connection.mav.command_ack_send() #need params
                        connection.mav.camera_information_send()
                        state = STATE_IDLE
                      
                    #Message is valid
                    # Use the attribute
                    print('Mode: %s' % msg.mode)
            
        elif(state == STATE_IDLE):
                
            msg = connection.recv_match(blocking=True)
            
            if not msg: 
                pass
            if msg.get_type() == "BAD_DATA":
                if mavutil.all_printable(msg.data):
                    sys.stdout.write(msg.data)
                    sys.stdout.flush()
                else:
                    if msg.get_type() == "MAV_CMD_REQUEST_MSG" and msg.param1 == 262 :
                        connection.mav.mav_result_accepted_send() #need params
                            
                        state = STATE_SEND
            
            
            #TODO: wait for MAV_CMD_REQUEST_MSG with param1 = 262
            # implement relative portion of the camera protocol and move into SEND state
            
            
        elif(state == STATE_SEND):
            pass
                #
                # LOGIC FOR TAKING PHOTO HERE
                #
                
                #IMPLEMENT REST OF "interactive user-initiated image capture" sequence
        