import requests
import json
import watson_constants
import watson_emotional_tones
import watson_language_tones
import watson_social_tones
from requests.auth import HTTPBasicAuth

#main method for calling Watson's tone analyzer
def get_tone_analysis(text):
	auth = HTTPBasicAuth(watson_constants.USERNAME, watson_constants.PASSWORD)
	headers = {"Content-Type": watson_constants.CONTENT_TYPE}
	payload = { "text": text }
	url = watson_constants.URL
	response = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))
	return response.text

def calculate_emotional_tones(text):
	emotion_dict = {}
	watson_data = json.loads(get_tone_analysis(text))
	tone_categories = watson_data["document_tone"]["tone_categories"]
	emotion_category_tone = filter(lambda x: x["category_id"] == "emotion_tone", tone_categories)[0]
	emotion_tones = emotion_category_tone["tones"]
	
	return emotion_tones

def calculate_language_tones(text):
	language_dict = {}
	watson_data = json.loads(get_tone_analysis(text))
	tone_categories = watson_data["document_tone"]["tone_categories"]
	language_category_tone = filter(lambda x: x["category_id"] == "language_tone", tone_categories)[0]
	language_tones = language_category_tone["tones"]

	return language_tones

def calculate_social_tones(text):
	social_dict = {}
	watson_data = json.loads(get_tone_analysis(text))
	tone_categories = watson_data["document_tone"]["tone_categories"]
	social_category_tone = filter(lambda x: x["category_id"] == "social_tone", tone_categories)[0]
	social_tones = social_category_tone["tones"]

	return social_tones	

def dominant_emotional_tone(text):
	emotion_tones = calculate_emotional_tones(text)
	dominant_emotion_tone = max(emotion_tones, key=lambda x: x["score"])

	return dominant_emotion_tone["tone_name"]

def dominant_language_tone(text):
	language_tones = calculate_language_tones(text)
	dominant_language_tone = max(language_tones, key=lambda x: x["score"])

	return dominant_language_tone["tone_name"]

def dominant_social_tone(text):
	social_tones = calculate_social_tones(text)
	dominant_social_tone = max(social_tones, key=lambda x: x["score"])

	return dominant_social_tone["tone_name"]