from flask import Flask, render_template, request
import json
#from cv2 import *
import time
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
        alt = int(request.form['alt'])
        fs = int(request.form['fs'])
        fo = int(request.form['fo'])
        co = int(request.form['co'])
        corient = request.form['corientname']
        gsd = int(request.form['gsd'])
        area = int(request.form['area'])
        ioname = request.form['ioname']

        if corient == 
        width = 
        height = 
        disBetCap = 
        disBetTrack = 
        tBetCap = 
        flightTime = 
        numCap = 
        numImg = 
        areaPerHour = 
        ssr = 

    return render_template('settings.html', width=width)