# Software Simulator

Software In The Loop (SITL) is a simulator that allows running ArduPilot without hardware. Using this, we are able to simulate running CUSP without having to connect to the flight controller and cameras.

There are two ways of running SITL: with the official ArduPilot codebase or using DroneKit-SITL. DroneKit-SITL does not have as many pre-built vehicles, but is significantly easier to install and run. In this project, we will be using DroneKit-SITL.

https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html
https://dronekit-python.readthedocs.io/en/latest/develop/sitl_setup.html

To install DroneKit-SITL:
`pip install dronekit-sitl -UI`

To run DroneKit-SITL:
`dronekit-sitl copter`
SITL starts and waits for a TCP connection at 127.0.0.1:5760

Using SITL instead of a UART connection to MAVLink is quite easy, just a drop-in replacement in the Python code.

Connection with UART on a Raspberry Pi to a Flight Controller:
```
...
    the_connection = mavutil.mavlink_connection('/dev/serial0', baud=57600, source_system=1, source_component=2)
...
```

Connection with SITL
```
...
    the_connection = mavutil.mavlink_connection('tcp:127.0.0.1:5760', baud=57600, source_system=1, source_component=2)
...
```

## Example of running a simulation


Process to manually test a simulated flight:
Activate SITL process 
```
cd ~/ardupilot/ArduCopter
../Tools/autotest/sim_vehicle.py --map --console
```
OR
```
dronekit-sitl copter --home=-35.363261,149.165230,584,353 # Can change coords
```
Connect to SITL with MAVProxy. Open a new terminal and run,
```
mavproxy.py --master tcp:127.0.0.1:5760
```
Add MAVLink output so that we can connect another application to SITL. In terminal running MAVProxy:
```
output add 127.0.0.1:14550
```
Connect to MAVProxy with our application via address udp:127.0.0.1:14550
Run flight. This simulated flight takes the drone to 40m, and flies in a 2000m circle. In MAVProxy terminal:
```
mode guided
arm throttle
takeoff 40
mode circle
param set circle_radius 2000
```