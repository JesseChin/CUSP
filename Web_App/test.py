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

'''@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html', items=items)'''

'''@app.route('/about/<username>')
def about_page(username):
    return f'<h1>About Page of {username}</h1>'''

@app.route('/getImage')
def get_img():
    return "test.jpg"

@app.route('/camSettings', methods = ['POST', 'GET'])
def cam_settings_page():
    output = request.form.to_dict()
    name = output["name"]

    return render_template('settings.html')

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