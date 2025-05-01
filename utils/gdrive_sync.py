import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Define the required scope for readonly access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_drive():
    """Authenticate and return a Google Drive service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def download_files_from_folder(service, folder_id, download_path='receipts/'):
    """Download all .jpg images from the specified Google Drive folder."""
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    query = f"'{folder_id}' in parents and mimeType='image/jpeg' and trashed=false"
    results = service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])

    for file in files:
        file_id = file['id']
        file_name = file['name']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(os.path.join(download_path, file_name), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f"Downloaded: {file_name}")