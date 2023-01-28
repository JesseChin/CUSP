# CUSP

[github link](https://github.com/JesseChin/CUSP)

## Project Description

The Compact UAV Sensor Package (CUSP) is a low-cost camera sensor package with a
longwave infrared (LWIR, 8 μm to 14 μm) and a high-resolution RGB camera for use with UAV remote sensing. The package is being developed as part of NASA Land Cover and Land Use Change and Ecosystems priority topic for NASA SERVIR-WA (West Africa) and for the Center for Remote Sensing and Geographic Information Services (CERSGIS), collaborating with the Environmental Protection Agency in Ghana. The purpose of these sensors is to combat deforestation and land degradation by monitoring illegal charcoal production and Galamsey operations (illegal small-scale gold mining). A machine learning model will be created to recognize these sites and report to the operator live.

CUSP is a unique low cost and lightweight product that provides on-board Machine Learning processing, a simple web configuration portal, and is fully open-source. Existing commercial solutions which provide live on-board image recognition do exist, though they are not open-source and certainly not budget-friendly. Existing open-source implementations, such as Imaging Package for Remote Vehicles (imPROV) do not provide ML capabilities, rely on 4G to operate, and occupy a large volume. CUSP is the only low-cost, small, and open-source sensor capable of monitoring illegal charcoal production and Galamsey.

---
## Requirements

### Hardware
- Raspberry Pi 3/4 or Jetson Nano
- Mavlink Capable Flight Controller
- 15-pin Raspberry Pi Compatible Camera
- Flir Lepton Thermal Imaging Sensor

### Software
- Python 3.9.2+
- Pymavlink
- Flask

---
## System Diagram

![System Diagram](/docs/RPI_Connection_Diagram.png)

---
## Component Explanation

`MAVLINK_Camera` is a folder containing test scripts intended to run on the raspberry pi. `mavlink_test.py` tests the mavlink connection and `camera_get.py` tests the attached camera.

The `Web_App` folder contains all the files needed to host the web server on the Pasberry Pi. the server is written in python with Flask and html.

The `docs` folder will contain any extra documentation as the project develops. For example, `gcs_test_msg.PNG` and `gcs_test_msg1.PNG` show that `mavlink_test.py` is functional.

---
## Setup
to use the Lepton sensor we needed to modify the kernel of the Pi. [This guide](https://github.com/FLIR/Lepton/blob/main/docs/RaspberryPiGuide.md) worked for us.

Now to install pymavlink, run these commands:

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