import datetime
import os

from models import Video
from video_validation import VideoValidation


def save_as_temp_file(file):
    """Save the given file as a temporary file and return the path of the saved file."""
    # Create a temporary file
    new_directory_path = os.path.join("media/", 'temp/')
    if not os.path.exists(new_directory_path):
        os.mkdir(new_directory_path)
    save_path = os.path.join(new_directory_path, file.filename)
    file.save(save_path)
    return save_path


def save_original_file(tmp_file_path: str, video_validator: VideoValidation, session):
    """Move the temporary video file to a permanent location, update database, and store the video."""
    save_path = "media/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    uuid_filename = video_validator.get_unique_filename()
    video_path = os.path.join(save_path, uuid_filename)
    import shutil
    shutil.move(tmp_file_path, video_path)

    # database store
    new_video = Video(video_name=video_validator.file_name, video_path=video_path)
    session.add(new_video)
    session.commit()


def get_search_result(search_string, session):
    """Search and return a list of video information based on the given search string and session."""
    search_result = []

    if type(search_string) == datetime.date:
        videos = session.query(Video).filter(Video.created_at.like(f'%{search_string}%')).all()
    else:
        videos = session.query(Video).filter(Video.video_name.like(f'%{search_string}%')).all()

    for video in videos:
        search_result.append(
            {
                "vide_name": video.video_name,
                "video_url": video.video_path,
                "uploaded_date": video.created_at.date().strftime('%Y-%m-%d'),
                "uploaded_time": video.created_at.time().strftime('%H:%M:%S')
            }
        )

    return search_result


def video_charge(video_size: int, video_duration: int):
    """Calculate the total charge based on the video size and duration."""
    total_charge = 0
    total_charge += 5 if video_size <= 500 else 12.5
    total_charge += 12.5 if video_duration <= 378 else 20
    return total_charge
