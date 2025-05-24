import googleapiclient.discovery
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

import crediantials  # Ensure this module contains required credentials


def check_drive_credentials():
    print("\n🔍 Checking Google Drive credentials...")
    CLIENT_ID = crediantials.GOOGLE_DRIVE_CLIENT_ID
    CLIENT_SECRET = crediantials.GOOGLE_DRIVE_CLIENT_SECRET
    REFRESH_TOKEN = crediantials.GOOGLE_DRIVE_REFRESH_TOKEN

    try:
        drive_creds = Credentials(
            token=None,
            refresh_token=REFRESH_TOKEN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )

        drive_service = googleapiclient.discovery.build("drive", "v3", credentials=drive_creds)
        drive_service.files().list(pageSize=1).execute()

        print("✅ Google Drive refresh token is valid.")
        return True

    except RefreshError as error:
        print("❌ Google Drive token refresh failed:", str(error))
        return False

    except HttpError as error:
        print("⚠️ Google Drive API error:", str(error))
        return False

    except Exception as e:
        print("⚠️ Unexpected error checking Drive credentials:", str(e))
        return False


def check_youtube_credentials():
    print("\n🔍 Checking YouTube credentials...")
    CLIENT_ID = crediantials.GOOGLE_YOUTUBE_CLIENT_ID
    CLIENT_SECRET = crediantials.GOOGLE_YOUTUBE_CLIENT_SECRET
    REFRESH_TOKEN = crediantials.GOOGLE_YOUTUBE_REFRESH_TOKEN
    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    try:
        youtube_creds = Credentials(
            token=None,
            refresh_token=REFRESH_TOKEN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=SCOPES,
        )

        youtube_service = googleapiclient.discovery.build("youtube", "v3", credentials=youtube_creds)
        youtube_service.channels().list(part="snippet", mine=True).execute()

        print("✅ YouTube refresh token is valid.")
        return True

    except RefreshError as error:
        print("❌ YouTube token refresh failed:", str(error))
        return False

    except HttpError as error:
        print("⚠️ YouTube API error:", str(error))
        return False

    except Exception as e:
        print("⚠️ Unexpected error checking YouTube credentials:", str(e))
        return False


def check_credentials():
    if check_drive_credentials() and check_youtube_credentials():
        print("\n✅ Both Google Drive and YouTube credentials are valid.")
        print("🚀 You can proceed with the script.")
        return True
    else:
        print("\n⛔ Aborting YouTube check due to Drive credential failure.")
        return False


if __name__ == "__main__":
    check_credentials()
