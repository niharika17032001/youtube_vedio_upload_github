import sys

import download_folder_from_drive
import upload_folder_to_drive
import youtube_upload
from check_google_refresh_token import check_credentials


def main():
    if check_credentials():
        # download_folder_from_drive.main()
        # youtube_upload.main()
        # upload_folder_to_drive.main()
        print("\n🎉 All tasks completed successfully!")
    else:
        print("\n⛔ Aborting YouTube check due to Drive credential failure.")
        sys.exit(1)
        print("\n🎉 All tasks completed successfully!")


if __name__ == "__main__":
    main()
