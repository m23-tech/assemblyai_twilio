# get_audio_data.py

import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client

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

        # Print the Results
        print(recording.call_sid)
        print(recording.uri)
    except Exception as error:
        print(f"Error Occurred: {error}")  

if __name__ == '__main__':
    rec_id = 'XXXXX' # ADD THE PROPER Recording SID
    get_recording_metadata(rec_id)
