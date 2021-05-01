# upload_and_transcribe.py

import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import json

# Identify the .env file in the local environment
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get the AssemblyAI API Key
assemblyai_key = os.environ['ASSEMBLYAI_API_KEY']

# Read the file  
def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


# Upload the file
def upload_file(file):
    try:
        headers = {'authorization':  assemblyai_key}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                headers=headers,
                                data=read_file(file))
        return response.json()
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


# Submit and Get the Transcribed Audio
def transcribe_audio(upload_url):
    try:
        audio_file = {'audio_url': upload_url}
        headers = {
            "authorization": assemblyai_key,
            "content-type": "application/json"
        }
        
        # Submit the audio file for be transcribed using the uploaded URL
        response = requests.post('https://api.assemblyai.com/v2/transcript',
                                headers=headers,
                                json=audio_file)
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
    # Downloaded fIle location (Twilio Downloaded File)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = "RE14ce0cec673e922d585a7bf6b8eb3100.mp3"
    file_path= f"{dir_path}\\{file_name}"
    print(f"Audio File Path: {file_path}")
    
    # Upload the File to AssemblyAI
    upload_response = upload_file(file_path)
    print(f"AssemblyAI Upload Path: {upload_response}")

    # Transcribe the Audio File
    result_data = transcribe_audio(upload_response['upload_url'])
    print(f"\nRESULT => {result_data}")

