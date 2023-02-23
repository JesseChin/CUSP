from flask import Flask, render_template, request
import json
import math
#from cv2 import *
import time

LEPTON_HFOV = 45.6
LEPTON_VFOV = 34.2

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    # insert live view code
    return render_template('home.html')

@app.route('/settings')
def settings_page():
    return render_template('settings.html')

@app.route('/getImage')
def get_img():
    return "test.jpg"

@app.route('/configuration')
def config_page():
    return render_template('config.html')

@app.route('/save', methods=['POST'])
def save_json():
    form_data = request.form
    data = json.dumps(form_data)
    with open('form_data.json', 'w') as outfile:
        json.dump(data, outfile)
    return render_template('config.html', show_alert=True)

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    width = None

    if request.method == 'POST':
        try:
            Altitude = int(request.form['alt'])
            Flight_Speed = int(request.form['fs'])
            Forward_Overlap = int(request.form['fo']) / 100.0
            Cross_Overlap = int(request.form['co']) / 100.0
            Camera_Orientation = request.form['corientname']
            Ground_Sampling_Distance = int(request.form['gsd'])
            Field_Area = int(request.form['area'])
            File_Format = request.form['ioname']

            Footprint_Width = 2*math.tan(math.radians(LEPTON_HFOV/2))*Altitude
            Footprint_Height= 2*math.tan(math.radians(LEPTON_VFOV/2))*Altitude
            if (Camera_Orientation == "Portrait"):
                Footprint_Width, Footprint_Height = Footprint_Height, Footprint_Width # swap
            Distance_Between_Capture = (Footprint_Height)*(1 - Forward_Overlap)
            Distance_Between_Track = (Footprint_Width)*(1 - Cross_Overlap)
            Time_Between_Capture = (Distance_Between_Capture)/(Flight_Speed)
            Number_of_Captures = 4046.86*Field_Area/(Footprint_Width*Footprint_Height*(1 - Forward_Overlap))
            Flight_Time = Time_Between_Capture
            Number_of_Images = 2*Number_of_Captures
            Area_per_Hour = (Footprint_Width*Footprint_Height*(1 - Forward_Overlap))/Time_Between_Capture * 3600/4046.86
            Storage_Space_Requirement = 50000*Number_of_Images # this is a placeholder value
        except:
            return render_template('settings.html', show_alert=True)

    return render_template('settings.html', width=Footprint_Width, height=Footprint_Height, disBetCap=Distance_Between_Capture, disBetTrack=Distance_Between_Track, tBetCap=Time_Between_Capture, flightTime=Flight_Time, numCap=Number_of_Captures, numImg=Number_of_Images, areaPerHour=Area_per_Hour, ssr=Storage_Space_Requirement)