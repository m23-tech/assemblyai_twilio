# download_multiple.py

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

def get_call_metadata():
    try:
        # Get call recordings
        recordings = client.recordings.list(limit=20)

        for record in recordings:
            recording_data = [record.uri,record.sid,record.call_sid,record.account_sid]
            download_file(recording_data)
    except Exception as error:
        print(f"Error Occurred: {error}")  


def download_file(url_data):
    # Separate list into variables
    uri_data = url_data[0]
    sid_data = url_data[1]
    call_data = url_data[2]
    account_data = url_data[3]

    try:
    # Create the download URL
        url = f'https://api.twilio.com{uri_data.replace(".json",".mp3")}'

        # Download and save the file within a new directory structure
        # Directory will be Account ID/Call SID/
        audio_file = requests.get(url)
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Create the mp3 file using the Recording SID as filename within the specified directory
        filename = f'{dir_path}\\{account_data}\\{call_data}\\{sid_data}.mp3'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as file:
            file.write(audio_file.content)
    except Exception as error:
        print(f"Error Occurred: {error}")  

if __name__ == '__main__':        
    get_call_metadata()