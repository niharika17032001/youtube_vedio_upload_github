import json
import os

import googleapiclient.discovery
import googleapiclient.http
from google.oauth2.credentials import Credentials
from gradio_client import Client, handle_file
from moviepy.editor import VideoFileClip
from tqdm import tqdm

import ImportantVariables
import crediantials
import download_folder_from_drive

# Replace with your actual credentials
CLIENT_ID = crediantials.GOOGLE_YOUTUBE_CLIENT_ID
CLIENT_SECRET = crediantials.GOOGLE_YOUTUBE_CLIENT_SECRET
REFRESH_TOKEN = crediantials.GOOGLE_YOUTUBE_REFRESH_TOKEN
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def set_thumbnail(youtube, video_id: str, thumbnail_path: str):
    """Sets a custom thumbnail for a given video."""
    if not os.path.exists(thumbnail_path):
        print(f"Thumbnail file not found: {thumbnail_path}")
        return

    print(f"Uploading thumbnail for video ID: {video_id}")
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=googleapiclient.http.MediaFileUpload(thumbnail_path)
    )
    response = request.execute()
    print("Thumbnail uploaded successfully.")
    return response
def get_video_duration(video_path):
    """Returns duration in seconds and minutes for a video file."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File not found: {video_path}")

    clip = VideoFileClip(video_path)
    duration_seconds = clip.duration
    duration_minutes = duration_seconds / 60
    clip.close()

    return round(duration_seconds, 2), round(duration_minutes, 2)
def get_video_paths(directory: str, extensions=None) -> list[str]:
    if extensions is None:
        extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv']

    video_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                video_paths.append(os.path.join(root, file))

    return video_paths





def read_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_authenticated_service():
    """Build and return an authenticated YouTube API service."""
    credentials = Credentials(
        token=None,  # Not used with refresh token
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri='https://oauth2.googleapis.com/token',
        scopes=SCOPES
    )

    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )

def add_shorts_tag(title: str, description: str) -> tuple[str, str]:
    """Ensure #Shorts is present in both title and description."""
    tag = "#Shorts"

    if tag.lower() not in title.lower():
        title += f" {tag}"
    if tag.lower() not in description.lower():
        description += f" {tag}"

    return title.strip(), description.strip()

def upload_video(youtube, file_path, title, description, category_id, keywords, privacy_status):
    """Uploads a video to YouTube with a tqdm progress bar."""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
            "tags": keywords,
        },
        "status": {"privacyStatus": privacy_status},
    }

    media = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    response = None
    progress_bar = tqdm(total=100, desc="Uploading", unit="%")

    last_progress = 0
    while response is None:
        status, response = request.next_chunk()
        if status:
            current_progress = int(status.progress() * 100)
            progress_bar.update(current_progress - last_progress)
            last_progress = current_progress

    progress_bar.close()
    print(f"\n✅ Video id '{response['id']}' was successfully uploaded.")
    return response

def main_setup_for_upload_video(json_data):
    youtube = get_authenticated_service()

    category_id = "22"  # Example: People & Blogs
    keywords = ["video", "upload", "api"]
    privacy_status = "public"

    for i, item in enumerate(json_data):

        raw_title = item.get('title')
        raw_description =item.get('description')

        video_id=item.get('video_id')
        thumbnail_id=item.get('thumbnail_id')

        path=download_folder_from_drive.download_file_from_drive(video_id)
        thumbnail_path=download_folder_from_drive.download_file_from_drive(thumbnail_id)



        print(f"Title: {raw_title}")
        print(f"Description: {raw_description}")
        print(f"Video Path: {path}")
        print(f"Thumbnail Path: {thumbnail_path}")


        title, description = add_shorts_tag(raw_title, raw_description)


        try:
            clip = VideoFileClip(path)
            duration = clip.duration
            print(f"Original video duration: {round(duration, 2)} seconds")

            if duration > 59:

                client = Client("amit0987/hf-vedio-cut")
                # Call the API with the video file (remove extra quotes in the path)
                # Define your inputs
                video_file = handle_file(path)
                start_time = 0
                end_time = 59

                # Call the API with all required inputs
                result = client.predict(
                    video_path={"video": video_file},  # Input 1: video
                    start_time=start_time,
                    end_time=end_time,  # Input 3: end time in seconds
                    api_name="/predict"
                )

                path = result['video']

            clip.close()

        except Exception as e:
            print(f"Error processing {path}: {e}")

        response = upload_video(youtube, path, title, description, category_id, keywords, privacy_status)
        video_id = response['id']
        print(f"video_id_{i}:{video_id}")

def main(max_videos= 1 ):
    metadata_file_json_file = ImportantVariables.metadata_file_json_file
    json_data = read_json_file(metadata_file_json_file)

    if max_videos < 0:
        max_videos = len(json_data)


    try:
        main_setup_for_upload_video(json_data[:max_videos])


    except Exception as e:
        print(f"Error processing video: {e}")

    finally:
        print("Upload process completed.")

    with open(metadata_file_json_file, "w") as json_file:
        json.dump(json_data[max_videos:], json_file, indent=4)




if __name__ == "__main__":
    main()
