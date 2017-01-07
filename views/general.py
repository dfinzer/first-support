import json
from app import app
from flask import render_template
import requests
import os
from flask import request, flash, redirect

EMOVU_WEB_API_BASE_URL = "http://api.emovu.com/api/imageframe"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/signal', methods=["POST"])
def signal():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            form_data = {
                "timestamp": 0,
                "previousFrameResult": ""
            }
            resp = requests.post(EMOVU_WEB_API_BASE_URL, data=form_data, headers={
                'LicenseKey': "57101804707473939007536796840064911726102607109433933006736111970083711786"
            }, files={"imageFile": f}).json()
            print resp
            return json.dumps(resp)
