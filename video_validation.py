import os.path
import uuid

import cv2


class VideoValidation:

    def __init__(self, tmp_file_path):
        self.tmp_file_path = tmp_file_path
        self.file_name = os.path.basename(tmp_file_path)
        self.video_type = self.file_name.split('.')[-1]
        self.allowed_extensions = ('.mp4', '.mkv')
        self.file_size_in_kb = None
        self.file_size_in_mb = None

    def is_validate_extensions(self):
        """Check if the file name has a valid video extension."""
        return self.file_name.endswith(self.allowed_extensions)

    def get_file_size(self):
        """Calculate and return the size of the temporary file in GB."""
        file_stat = os.stat(self.tmp_file_path)
        file_size_in_bytes = file_stat.st_size
        self.file_size_in_kb = file_size_in_bytes / 1024
        self.file_size_in_mb = self.file_size_in_kb / 1024
        file_size_in_gb = self.file_size_in_mb / 1024
        return file_size_in_gb

    def get_file_duration(self):
        """Calculate and return the duration of the video in seconds."""
        try:
            # create video capture object
            print("get_video", self.tmp_file_path)
            data = cv2.VideoCapture(self.tmp_file_path)

            if not data.isOpened():
                raise ValueError("Failed to open the video file.")

            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)

            # calculate duration of the video
            seconds = round(frames / fps)

            return seconds
        except Exception as e:
            print("Error:", e)
            return None

    def get_unique_filename(self):
        """Generate and return a unique filename with the video type extension."""
        return f"{uuid.uuid4().hex}.{self.video_type}"
