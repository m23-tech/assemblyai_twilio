# url_and_transcribe.py

import os
import time
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client
import requests
import json

# Identify the .env file in the local environment
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Load the details from .env file
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
assemblyai_key = os.environ['ASSEMBLYAI_API_KEY']

def get_recording_metadata(recording_id):
    try:
        # Get the Metadata
        recording = client.recordings(recording_id).fetch()
        # Get the URL
        return recording.uri
    except Exception as error:
        print(f"Error Occurred: {error}")  

# Get the Transcribed Result
def get_result(transcribe_id):
    try:
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transcribe_id}"
        headers = {'authorization':  assemblyai_key}
        response = requests.get(endpoint, headers=headers)

        result = json.loads(response.content)
        # When completed return the resulting text
        if result['status'] == 'completed':
            text_result = result['text']
            return text_result
        elif result['status'] == 'queued' or result['status'] == 'processing':
            print("=====Processing Result====")
            time.sleep(20)
        elif result['status'] == 'error':
            error = "Please Try Again"
            return error
    except Exception as error:
        print(f"Error Occurred: {error}")  

def transcribe_audio(upload_url):
    try:
        endpoint = "https://api.assemblyai.com/v2/transcript"
        audio_file = {'audio_url': upload_url}
        headers = {
            "authorization": assemblyai_key,
            "content-type": "application/json"
        }

        response = requests.post(endpoint, json=audio_file, headers=headers)
        response_data = json.loads(response.content)
        print(f"AssemblyAI Transcription ID: {response_data['id']}")

        # Loop to obtain the result
        transcription = None
        while True:
            # Call the get_result function
            transcription = get_result(response_data['id'])
            if transcription is not None:
                break
        
        return transcription
    except Exception as error:
        print(f"Error Occurred: {error}")  

if __name__ == '__main__':
    rec_id = 'RE14ce0cec673e922d585a7bf6b8eb3100'
    uri_data = get_recording_metadata(rec_id)
    print(f"Twilio URI: {uri_data}")

    # Create the download URL
    url = f'https://api.twilio.com{uri_data.replace(".json",".mp3")}'
    print(f"Twilio Audio File URL: {url}")

    # Get the transcribed result
    result_data = transcribe_audio(url)
    print(f"\nRESULT => {result_data}")