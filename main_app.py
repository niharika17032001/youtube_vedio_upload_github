import download_folder_from_drive
import upload_folder_to_drive
import youtube_upload


def main():
    download_folder_from_drive.main()
    youtube_upload.main()
    upload_folder_to_drive.main()


if __name__ == "__main__":
    main()