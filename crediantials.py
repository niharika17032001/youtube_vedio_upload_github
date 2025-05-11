from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_YOUTUBE_CLIENT_ID = os.getenv("GOOGLE_YOUTUBE_CLIENT_ID")
GOOGLE_YOUTUBE_CLIENT_SECRET = os.getenv("GOOGLE_YOUTUBE_CLIENT_SECRET")
GOOGLE_YOUTUBE_REFRESH_TOKEN = os.getenv("GOOGLE_YOUTUBE_REFRESH_TOKEN")

GOOGLE_DRIVE_CLIENT_ID = os.getenv("GOOGLE_DRIVE_CLIENT_ID")
GOOGLE_DRIVE_CLIENT_SECRET = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
GOOGLE_DRIVE_REFRESH_TOKEN = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN")


file_path = os.path.abspath(__file__)
current_Folder_Path = os.path.dirname(file_path)
root_folder = os.path.dirname(current_Folder_Path)

print(f"Current Folder Path: {current_Folder_Path}")
print(f"Root Folder Path: {root_folder}")
screenshot_path = current_Folder_Path + '/reports/screenshot.png'
page_content_path = current_Folder_Path + '/reports/page_content.html'
video_path = current_Folder_Path + '/reports'

required_secrets = {
    "GOOGLE_YOUTUBE_CLIENT_ID": GOOGLE_YOUTUBE_CLIENT_ID,
    "GOOGLE_YOUTUBE_CLIENT_SECRET": GOOGLE_YOUTUBE_CLIENT_SECRET,
    "GOOGLE_YOUTUBE_REFRESH_TOKEN": GOOGLE_YOUTUBE_REFRESH_TOKEN,
    "GOOGLE_DRIVE_CLIENT_ID": GOOGLE_DRIVE_CLIENT_ID,
    "GOOGLE_DRIVE_CLIENT_SECRET": GOOGLE_DRIVE_CLIENT_SECRET,
    "GOOGLE_DRIVE_REFRESH_TOKEN": GOOGLE_DRIVE_REFRESH_TOKEN,
}

for key, value in required_secrets.items():
    if not value:
        raise ValueError(f"{key} is missing. Ensure it is set in GitHub Secrets.")



