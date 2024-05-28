from __future__ import unicode_literals
from __future__ import print_function
from pydub import AudioSegment
import os
import yt_dlp as youtube_dl
from moviepy.editor import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import glob

# Put your songs in a file named input.txt formatted like so:
# Line 1 - Name of the folder to put the files
# Other Lines - https://www.youtube.com/examplesong, FileName, minutestamp:secondstamp

def clipToSize(name, timestamp):
    AudioSegment.from_mp3(name + "temp.mp3").export(name + "temp.wav", format="wav")
    os.remove(name + 'temp.mp3')
    AudioSegment.from_wav(name + "temp.wav").export(name + "temp.mp3", format="mp3")
    os.remove(name + "temp.wav")
    song = AudioSegment.from_mp3(name + "temp.mp3")
    print(timestamp)
    extract = song[1000*timestamp:1000*timestamp + 40000]
    print(extract.duration_seconds)
    os.remove(name + 'temp.mp3')
    extract.export(name + ".mp3", format="mp3")

def uploadFolderToDrive(source_name):
    folder_metadata = {
            'name': [source_name],
            'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    return folder_id
 
def downloadFile(url, name, timestamp):
    ydl_opts = {
        'outtmpl': './' + name + '.mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    file_name = glob.glob(name + '.*')[0]
    video = VideoFileClip(file_name)
    video.audio.write_audiofile(name + "temp.mp3")
    video.close()
    os.remove(file_name)
    clipToSize(name, timestamp)
def downloadFiles(source_name):
    folder_name = ""
    folder_id = ""
    source_file = open(source_name, 'r')
    lines = source_file.readlines()
    for index, line in enumerate(lines):
        if index == 0:
            folder_name = line
            folder_id = uploadFolderToDrive(folder_name)
        else:
            line_array = line.split(", ")
            url = line_array[0]
            name = line_array[1]
            timestamp = int(line_array[2].split(":")[0].strip())*60 + int(line_array[2].split(":")[1].strip())
            downloadFile(url, name, timestamp)
            file_metadata = {
                'name': [name],
                'parents': [folder_id]
            }
            media = MediaFileUpload("./" + name + ".mp3", mimetype='audio/mpeg', resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('File ID: ' + file.get('id'))
            os.remove(name + ".mp3")
    return folder_name

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)
downloadFiles("input.txt")