# CUSP

[github link](https://github.com/JesseChin/CUSP)

## Project Description

The Compact UAV Sensor Package (CUSP) is a low-cost camera sensor package with a longwave infrared (LWIR, 8 μm to 14 μm) and a high-resolution RGB camera for use with UAV remote sensing. The package is being developed as part of NASA Land Cover and Land Use Change and Ecosystems priority topic for NASA SERVIR-WA (West Africa) and for the Center for Remote Sensing and Geographic Information Services (CERSGIS), collaborating with the Environmental Protection Agency in Ghana. The purpose of these sensors is to combat deforestation and land degradation by monitoring illegal charcoal production and Galamsey operations (illegal small-scale gold mining). A machine learning model will be created to recognize these sites and report to the operator live.

CUSP is a unique low cost and lightweight product that provides on-board Machine Learning processing, a simple web configuration portal, and is fully open-source. Existing commercial solutions which provide live on-board image recognition do exist, though they are not open-source and certainly not budget-friendly. Existing open-source implementations, such as Imaging Package for Remote Vehicles (imPROV) do not provide ML capabilities, rely on 4G to operate, and occupy a large volume. CUSP is the only low-cost, small, and open-source sensor capable of monitoring illegal charcoal production and Galamsey.

---
## Screenshots

![estimator_screenshot](/docs/Screenshots/estimator_screenshot.jpg)

![config_screenshot](/docs/Screenshots/config_screenshot.jpg)

---
## Requirements

### Hardware
- Raspberry Pi 3/4 or Jetson Nano (todo)
- MAVLink Capable Flight Controller
- 15-pin Raspberry Pi Compatible Camera
- FLIR Lepton Thermal Imaging Sensor

### Software
- Python 3.9.2+
- Pymavlink
- Flask

---
## System Diagram

![System Diagram](/docs/System_Diagram_RPI.png)

![Raspberry Pi <---> Flight Control](/docs/RPI_Connection_Diagram.png)

---
## Component Explanation

`MAVLINK_Camera` is a folder containing test scripts intended to run on the raspberry pi. `get_params_test.py` and `mavlink_test.py` tests the MAVLink connection and `camera_get.py` tests the attached camera. `CUSP_camera.py` is the camera capturing module, `CUSP_error_types.py` is the error type module, `CUSP_gps.py` is the gps handling module, `CUSP_messages.py` is the module containing our message enumerations, `CUSP_trigger.py` is the moduel containing logic for specific event triggers, and finally `main.py` is the application stating point.

captured images are saved in the `$HOME/data` directory on the pi.

The `Web_App` folder contains all the files needed to host the web server on the Raspberry Pi. The server is written in Python with Flask and HTML+CSS. the static folder contains all the assets and the templates folder contains all the html files. `app.py` is the starting point.

The `docs` folder will contain any extra documentation as the project develops. For example, `gcs_test_msg.PNG` and `gcs_test_msg1.PNG` show that `mavlink_test.py` is functional.

The `sim` folder contains all our files to help simualte a flight controller in flight so we do not need to actually fly a drone to develop new featues. [This README](sim/README.md) contains much more info.

---
## Setup
To use the Lepton sensor we needed to modify the kernel of the Pi. [This guide](https://github.com/FLIR/Lepton/blob/main/docs/RaspberryPiGuide.md) worked for us.

MAVProxy is a convenient way to test the connection of the Pi and flight controller. It also installs pymavlink as a dependency:
```
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
pip3 install PyYAML mavproxy --user
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```

After that, installing Flask is simple:

```
pip install Flask
```

Now make sure the system is wired as shown in the [System Diagram](#System-Diagram), and you should be able to run our test scripts.

## Usage

to start the web server connect to the pi via SSH, navigate to the Web_App folder, and run the following command:

```
flask run --host=<ip_address>
```

where `<ip_address>` is replaced with the Pi's current ip address.

Once this is running you will be able to access the web interface through any web browser (we tested both Chrome and Firefox) by typing `http://<ip_address>:5000` into the address bar, once again replacing `<ip_address>` with the Pi's current ip address.

This whole process will hopefully be made much more user friendly in upcoming builds.

At this point there are two useful tabs, both of which can be accessed with the icons on the navigation bar on the top of the screen.

The first is the Pre-Flight Estimator. This tab allows the user to estimate the stats of a flight using already known variables. To learn the units of each variable, simply hover your mouse over it. When the user is ready they can select the large "Update Settings" button and they will either be greeted with an appropriate error message or the result of their flight.

The next useful tab is the Configuration Menu. This is where the data is configured for the actual flight. Once this data is filled the user can select the "Save" button, at which point they will receive a notification containing an appropriate error message or "JSON Saved"

[add section on if the web server crashes]

To begin a flight navigate to the pi_sim folder and run the following command:

```
python3 main.py
```

In the future this will be done from the web interface or started automatically once the Pi receives power.