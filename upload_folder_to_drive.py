import json
import os
import shutil

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import ImportantVariables as imp_val
import crediantials

# Replace with your actual credentials
CLIENT_ID = crediantials.GOOGLE_DRIVE_CLIENT_ID
CLIENT_SECRET = crediantials.GOOGLE_DRIVE_CLIENT_SECRET
REFRESH_TOKEN = crediantials.GOOGLE_DRIVE_REFRESH_TOKEN

# Construct credentials object
credentials = Credentials(token=None,  # Not used with refresh token
                          refresh_token=REFRESH_TOKEN, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                          token_uri='https://oauth2.googleapis.com/token', )

# Build the Drive API service
drive_service = build('drive', 'v3', credentials=credentials)


def copy_files_to_folder(files, destination_folder):
    """
    Copies a list of files to a specified folder.

    Args:
        files (list): List of file paths to copy.
        destination_folder (str): Path to the target folder.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)  # Create the folder if it doesn't exist

    for file in files:
        if os.path.exists(file):  # Check if the file exists
            shutil.copy(file, destination_folder)
            print(f"Copied: {file} -> {destination_folder}")
        else:
            print(f"File not found: {file}")


def prepare_imp_json_folder_to_upload(destination_folder):
    imp_json_files = [
        imp_val.metadata_file_json_file,
        imp_val.yt_links_for_facebook_json_file_path
    ]
    imp_json_files_folder = destination_folder + "/imp_json_files"

    copy_files_to_folder(imp_json_files, imp_json_files_folder)


def upload_folder_to_drive(local_folder_path, parent_drive_folder_id):
    """Uploads all files and subfolders from a local folder to a specified folder in Google Drive, overriding existing files."""
    if not os.path.exists(local_folder_path):
        print("Error: Folder does not exist.")
        return

    for item in os.listdir(local_folder_path):
        item_path = os.path.join(local_folder_path, item)

        if os.path.isdir(item_path):  # Handle subfolders
            subfolder_id = get_or_create_folder(item, parent_drive_folder_id)
            upload_folder_to_drive(item_path, subfolder_id)
        elif os.path.isfile(item_path):  # Handle files
            print(f"Uploading: {item}...")
            existing_file_id = get_existing_file_id(item, parent_drive_folder_id)

            if existing_file_id:
                print(f"File {item} already exists. Overriding...")
                drive_service.files().delete(fileId=existing_file_id).execute()

            file_metadata = {'name': item, 'parents': [parent_drive_folder_id]}
            media = MediaFileUpload(item_path, resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            print(f"Uploaded {item}, File ID: {file.get('id')}")


def get_existing_file_id(filename, parent_drive_folder_id):
    """Checks if a file with the given name exists in the specified Google Drive folder."""
    query = f"name = '{filename}' and '{parent_drive_folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None


def get_or_create_folder(folder_name, parent_drive_folder_id):
    """Checks if a folder exists in Google Drive, creates it if not, and returns its ID."""
    query = f"name = '{folder_name}' and '{parent_drive_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if files:
        return files[0]['id']

    file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder',
                     'parents': [parent_drive_folder_id]}
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')


def prepare_yt_links_for_facebook_json():
    filepath = imp_val.yt_links_for_facebook_json_file_path
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        main_dict = {}
        print("convert yt_links_for_facebook_json list into dict ")
        for i, id in enumerate(data):
            main_dict[i] = id

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(main_dict, f, indent=4, ensure_ascii=False)


def main():
    parent_drive_folder_id = imp_val.youtube_videos_for_upload_folder_id
    current_folder = imp_val.current_Folder_Path
    imp_json_folder_to_upload_path = current_folder + "/imp_json_folder_to_upload"

    prepare_yt_links_for_facebook_json()
    prepare_imp_json_folder_to_upload(imp_json_folder_to_upload_path)
    upload_folder_to_drive(imp_json_folder_to_upload_path, parent_drive_folder_id)


if __name__ == "__main__":
    main()
    # prepare_yt_links_for_facebook_json()
