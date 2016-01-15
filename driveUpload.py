#!/usr/bin/python

import httplib2
import pprint
from datetime import datetime

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets


# Copy your credentials from the APIs Console
CLIENT_ID = '503179181877-nn836qd8h7j9na6fjmnkuq1js4vte9e3.apps.googleusercontent.com'
CLIENT_SECRET = 'cF2Rw8V5rrD7wYTwptYAMBB9'

# Check https://developers.google.com/drive/scopes for all available scopes
path_to_json = "client_secrets.json"
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials
flow = flow_from_clientsecrets(path_to_json, OAUTH_SCOPE, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
authorize_url = flow.step1_get_authorize_url()

url = open("url_doidona.txt", "w")
url.write(authorize_url)
url.close()

print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)

body = {
 'title': 'My document',
 'description': 'A test document',
 'mimeType': 'text/plain',
 'start': {
   'timeZone': 'GMT-3',
   'dateTime': str(datetime.now())
 },
 'end': {
   'timeZone': 'GMT-3',
   'dateTime': str(datetime.now())
 }
}

print body

file = drive_service.files().insert(body=body, media_body=media_body).execute()

pprint.pprint(file)
