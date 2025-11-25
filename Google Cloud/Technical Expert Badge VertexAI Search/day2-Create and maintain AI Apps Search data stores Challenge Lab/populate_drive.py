import json
import glob
import os
import sys
import subprocess
import google.auth

from google.cloud import storage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

LOCAL_DOWNLOAD_PATH = "lab_drive_files"
BUCKET_NAME = "cloud-samples-data"
FOLDERS = [
    "generative-ai/image",
    "gen-app-builder/search/alphabet-investor-pdfs",
    "gen-app-builder/search/stanford-cs-224",
]
GOOGLE_DRIVE_FOLDER_NAME = "GCS_Backup"
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_gcloud_token():
    token = subprocess.run(
        ["gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    return token

# Authenticate Google Cloud Storage using gcloud token
def authenticate_gcs():
    token = get_gcloud_token()
    credentials = Credentials(token=token)
    return storage.Client(credentials=credentials)

# Download files from GCS
def download_from_gcs(client):
    bucket = client.bucket(BUCKET_NAME)

    for folder in FOLDERS:
        folder_path = os.path.join(
            LOCAL_DOWNLOAD_PATH, folder.replace("/", "_"))
        os.makedirs(folder_path, exist_ok=True)

        # Get up to 10 blobs in the folder
        blobs = [blob for blob in client.list_blobs(
            BUCKET_NAME, prefix=folder) if not blob.name.endswith("/")][:10]

        for blob in blobs:
            local_file_path = os.path.join(
                folder_path, os.path.basename(blob.name))
            print(f"Downloading {blob.name} to {local_file_path}")
            blob.download_to_filename(local_file_path)

def get_gcloud_project():
    """Retrieves the currently set GCP project using google.auth library."""
    creds, project = google.auth.default()
    return project  # Returns the active project ID or None

def find_token_dir():
    """Finds the most recent dir matching the pattern /tmp/tmp.*"""
    dirs = glob.glob("/tmp/tmp.*")  # Get all matching dirs
    if not dirs:
        return None  # No matching dirs found

    # Find the most recently modified dir
    most_recent_dir = max(dirs, key=os.path.getmtime)
    return most_recent_dir

def authenticate():
    """Authenticates the user and returns the Google Drive service."""
    creds = None
    token_file = f'{find_token_dir()}/application_default_credentials.json'


    # Load credentials if available
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            saved_creds = json.load(f)
            creds = Credentials.from_authorized_user_info(saved_creds, SCOPES)

    # If credentials are invalid or missing, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                './client_secrets.json', 
                SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            
            # Use manual authentication in Cloud Shell
            auth_url, _ = flow.authorization_url(prompt='consent')
            print("Please go to this URL and authorize access:", auth_url)

            # Ask the user to paste the authorization code
            auth_code = input("Enter the authorization code here: ").strip()
            flow.fetch_token(code=auth_code)

            creds = flow.credentials

        quota_project_id = get_gcloud_project()
        # Save credentials for future use
        with open(token_file, 'w') as token:
            new_creds = json.loads(creds.to_json())  # Convert to dictionary
            new_creds["quota_project_id"] = quota_project_id 
            token.write(json.dumps(new_creds, indent=2))

    return build('drive', 'v3', credentials=creds)


def create_drive_folder(service, folder_name, parent_id=None):
    print(folder_name, parent_id)
    """Creates a folder on Google Drive and returns its ID."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, spaces='drive',
                                   fields="files(id)").execute()
    if results.get('files'):
        return results['files'][0]['id']  # Return existing folder ID if found

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    print(f"Created folder: {folder_name} - ID: {folder['id']}")
    return folder['id']


def upload_file(service, file_path, parent_id):
    """Uploads a single file to Google Drive."""
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [parent_id]
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()

    print(f"Uploaded: {file_path} - ID: {file.get('id')}")
    return file.get('id')


def upload_directory(service, local_dir, parent_id=None):
    """Recursively uploads a directory (with all subdirectories and files) to Google Drive."""
    if not os.path.isdir(local_dir):
        print(f"Error: {local_dir} is not a directory.")
        return

    local_dir = os.path.normpath(local_dir)
    folder_name = os.path.basename(local_dir)
    folder_id = create_drive_folder(service, folder_name, parent_id)

    for item in os.listdir(local_dir):
        item_path = os.path.join(local_dir, item)

        if os.path.isdir(item_path):
            # Recursively upload subfolders
            upload_directory(service, item_path, folder_id)
        elif os.path.isfile(item_path):
            # Upload files to the correct folder
            upload_file(service, item_path, folder_id)


if __name__ == "__main__":
    gcs_client = authenticate_gcs()
    download_from_gcs(gcs_client)
    drive_service = authenticate()
    upload_directory(drive_service, LOCAL_DOWNLOAD_PATH)
