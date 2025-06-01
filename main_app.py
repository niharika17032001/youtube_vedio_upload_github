import sys

import clone_a_file_from_github
import download_folder_from_drive
import upload_folder_to_drive
import youtube_upload
from check_google_refresh_token import check_credentials


def main():
    clone_a_file_from_github.main()
    if check_credentials():
        download_folder_from_drive.main()
        youtube_upload.main()
        upload_folder_to_drive.main()
        print("\n🎉 All tasks completed successfully!")
    else:
        print("\n⛔ Aborting YouTube check due to Drive credential failure.")
        sys.exit(1)


if __name__ == "__main__":
    main()
