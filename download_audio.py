# download_audio.py

import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client
import requests

# Identify the .env file in the local environment
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Load the details from .env file
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def get_recording_metadata(recording_id):
    try:
        # Get the Metadata
        recording = client.recordings(recording_id).fetch()
        recording_data = [recording.uri,recording.sid]
        # Return the uri and sid as a list
        return recording_data
    except Exception as error:
        print(f"Error Occurred: {error}")  


def download_file(url_data):
    # Separate list into variables
    uri_data = url_data[0]
    sid_data = url_data[1]

    try:
        # Create the download URL
        url = f'https://api.twilio.com{uri_data.replace(".json",".mp3")}'

        # Download and save the file in the current directory
        audio_file = requests.get(url)
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Create the mp3 file using the Recording SID as filename
        with open(f'{dir_path}\\{sid_data}.mp3', 'wb') as file:
            file.write(audio_file.content)
    except Exception as error:
        print(f"Error Occurred: {error}")  

if __name__ == '__main__':
    rec_id = 'RE14ce0cec673e922d585a7bf6b8eb3100'
    url_info = get_recording_metadata(rec_id)
    download_file(url_info)