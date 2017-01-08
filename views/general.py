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
	
	avs_access = json.dumps(request.values.__dict__)
	badgenumber = request.values.get("officer")
	question_array = [
		"Have you experienced recurring, unwanted distressing memories of a work-related event.",
		"Have you experienced reliving the event as if it were happening again", 
		"Have you experienced trying to avoid thinking about a specific work-related event?",
		"Have you experienced avoiding places, objects, activities or people that remind you of the event?",
		"Have you experienced irritability, feeling tense or on guard? ", 
		"Have you experienced being on constant guard for danger? "
		]
		
	return json.dumps(question_array)
	#return json.dumps(request.values.__dict__)
	#return render_template('avs_return.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/store_interview', methods=["POST"])
def store_interview():
	if request.method == 'POST':
		posted = request.values.post
		#q_id = posted("question_id")
		q_answer = posted("answer")
	return json.dumps({"store_result":"true"})

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
            print(end - start, "TIMING FOR RESPONSE")
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

@app.route('/admin_index')
def admin_index():
	return render_template('admin_index.html')
	