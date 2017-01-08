import json
from app import app
from flask import render_template
from flask.helpers import url_for
import requests
import os
from app import r
from flask import request, flash, redirect

EMOVU_WEB_API_BASE_URL = "http://api.emovu.com/api/imageframe"

@app.route('/')
def index():
    return redirect(url_for('start'))

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/avs')
def avs():
    return render_template('avs.html')

@app.route('/avs_return')
def avs_return():
	avs_verify_url = "https://api.amazon.com/auth/O2/tokeninfo"
	avs_access = json.dumps(request.values.__dict__)
	access_token = request.values.get("access_token")
	verify = requests.get(avs_verify_url, params={"access_token":access_token}).json()
	print verify
	return json.dumps(resp)
	#return json.dumps(request.values.__dict__)
	#return render_template('avs_return.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/use_alexa')
def use_alexa():
	return render_template('use_alexa.html')

@app.route('/signal', methods=["POST"])
def signal():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            form_data = {
                "timestamp": 0,
                "previousFrameResult": ""
            }
            import time

            start = time.time()

            resp = requests.post(EMOVU_WEB_API_BASE_URL, data=form_data, headers={
                'LicenseKey': "57101804707473939007536796840064911726102607109433933006736111970083711786"
            }, files={"imageFile": f}).json()
            end = time.time()
            print(end - start, "YOOOO")
            data = json.dumps(resp)
            r.lpush("mood_points", data)
            return data



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/finish')
def finish():
    return render_template('finish.html')

@app.route('/pie')
def pie():
    return render_template('pie_chart.html')

@app.route('/dashboard_data')
def dashboard_data():
    data = [json.loads(x) for x in r.lrange('mood_points', 0, -1)]
    return json.dumps(data)
