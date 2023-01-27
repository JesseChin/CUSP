from pymavlink import mavutil

class PROG_STATE(Enum):
    INIT = 0
    IDLE = 1
    SEND = 2


if __name__ == "__main__":
    state = PROG_STATE.INIT
    
    connection = mavutil.mavlink_connection('/dev/serial0', baud=57600)
    
    connection.wait_heartbeat()
    
    connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_CAMERA, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    
    while(True):
        match state:
            case PROG_STATE.INIT:
            
                msg = the_connection.recv_match(blocking=True)
        
                if not msg:
                    #return
                if msg.get_type() == "BAD_DATA":
                    if mavutil.all_printable(msg.data):
                        sys.stdout.write(msg.data)
                        sys.stdout.flush()
                else:
                    if msg.get_type() == "MAV_CMD_REQUEST_MSG" and msg.param1 == 259 :
                        command_ack_send() #need params
                        camera_information_send()
                        state = PROG_STATE.IDLE
                      
            #Message is valid
            # Use the attribute
            print('Mode: %s' % msg.mode)
            
            case PROG_STATE.IDLE:
                
                msg = the_connection.recv_match(blocking=True)
            
                    if not msg:
                        #return
                    if msg.get_type() == "BAD_DATA":
                        if mavutil.all_printable(msg.data):
                            sys.stdout.write(msg.data)
                            sys.stdout.flush()
                    else:
                        if msg.get_type() == "MAV_CMD_REQUEST_MSG" and msg.param1 == 262 :
                            mav_result_accepted_send() #need params
                            
                            state = PROG_STATE.SEND
            
            
            #TODO: wait for MAV_CMD_REQUEST_MSG with param1 = 262
            # implement relative portion of the camera protocol and move into SEND state
            
            
            case PROG_STATE.SEND:
                #
                # LOGIC FOR TAKING PHOTO HERE
                #
                
                #IMPLEMENT REST OF "interactive user-initiated image capture" sequence
        