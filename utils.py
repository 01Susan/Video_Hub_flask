import os

from models import Video
from video_validation import VideoValidation


def save_as_temp_file(file):
    # Create a temporary file
    new_directory_path = os.path.join("media/", 'temp/')
    if not os.path.exists(new_directory_path):
        os.mkdir(new_directory_path)
    save_path = os.path.join(new_directory_path, file.filename)
    file.save(save_path)
    return save_path


def save_original_file(tmp_file_path: str, video_validator: VideoValidation, session):
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
