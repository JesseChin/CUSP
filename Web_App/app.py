from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileRequired
import json
import math
#from cv2 import *
import time

LEPTON_HFOV = 45.6
LEPTON_VFOV = 34.2

app = Flask(__name__)
app.secret_key = '0123456789'

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/models'
photos.extensions = ('pdf', 'pptx',)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField('ML Model:', validators=[FileRequired()])

@app.route('/')
@app.route('/home')
def home_page():
    # insert live view code
    return render_template('home.html', active_page='home_page')

@app.route('/settings')
def settings_page():
    form_data = {}
    return render_template('settings.html', form_data=form_data, active_page='settings_page')

@app.route('/getImage')
def get_img():
    return "test.jpg"

@app.route('/configuration')
def config_page():
    form = UploadForm()
    form_data = {}
    return render_template('config.html', form=form, form_data=form_data, active_page='config_page')

@app.route('/save', methods=['POST'])
def save_json():
    form_data = request.form
    data = json.dumps(form_data)
    with open('form_data.json', 'w') as outfile:
        json.dump(data, outfile)
    form_data = form_data.to_dict()
    return render_template('config.html', form_data=form_data, show_alert=True, active_page='config_page')

@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    form_data = {}
    if request.method == 'POST' and form.validate():
        filename = photos.save(request.files['photo'])
        return render_template('config.html', form=form, model_uploaded=True, form_data=form_data, active_page='config_page')
    return render_template('config.html', form=form, form_data=form_data, active_page='config_page')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    width = None
    form_data = request.form.to_dict()
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
        except:
            return render_template('settings.html', show_alert=True, active_page='settings_page')

        Footprint_Width = 2*math.tan(math.radians(LEPTON_HFOV/2))*Altitude
        Footprint_Height= 2*math.tan(math.radians(LEPTON_VFOV/2))*Altitude
        if (Camera_Orientation == "Portrait"):
            Footprint_Width, Footprint_Height = Footprint_Height, Footprint_Width # swap
        Distance_Between_Capture = (Footprint_Height)*(1 - Forward_Overlap)
        Distance_Between_Track = (Footprint_Width)*(1 - Cross_Overlap)
        Time_Between_Capture = (Distance_Between_Capture)/(Flight_Speed)
        Number_of_Captures = 4046.86*Field_Area/(Footprint_Width*Footprint_Height*(1 - Forward_Overlap))
        Flight_Time = Number_of_Captures*Time_Between_Capture
        Number_of_Images = 2*Number_of_Captures
        Area_per_Hour = (Footprint_Width*Footprint_Height*(1 - Forward_Overlap))/Time_Between_Capture * 3600/4046.86
        Storage_Space_Requirement = 1.94*Number_of_Images

        Footprint_Width = str(round(Footprint_Width, 2)) + " m"
        Footprint_Height = str(round(Footprint_Height, 2)) + " m"
        Distance_Between_Capture = str(round(Distance_Between_Capture, 2)) + " m"
        Distance_Between_Track = str(round(Distance_Between_Track, 2)) + " m"
        Time_Between_Capture = str(round(Time_Between_Capture, 2)) + " s"
        Number_of_Captures = str(round(Number_of_Captures, 1))
        Flight_Time = str(round(Flight_Time, 2)) + " s"
        Number_of_Images = str(round(Number_of_Images, 1))
        Area_per_Hour = str(round(Area_per_Hour, 2)) + " m^2/H"
        Storage_Space_Requirement = str(round(Storage_Space_Requirement, 2)) + " MB"

    return render_template('settings.html', form_data=form_data, width=Footprint_Width, height=Footprint_Height, disBetCap=Distance_Between_Capture, disBetTrack=Distance_Between_Track, tBetCap=Time_Between_Capture, flightTime=Flight_Time, numCap=Number_of_Captures, numImg=Number_of_Images, areaPerHour=Area_per_Hour, ssr=Storage_Space_Requirement, active_page='settings_page')