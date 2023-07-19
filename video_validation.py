import uuid
import os


class Video:

    def __init__(self, video_file):
        self.video_file = video_file
        self.filename = video_file.filename


    def validate_extensions(self):
        allowed_extensions = ('.mp4', '.mkv')
        if not self.file_name.endswith(allowed_extensions):
            return False

    def calculate_filesize(self):
        file_data = self.video_file.read()
        file_size = len(file_data)
        return file_size

    def get_file_duration(self):
        pass

    def unique_filename(self):
        extension = self.filename.split('.')[-1]
        return f"{uuid.uuid4().hex}.{extension}"

    def save_video(self):
        save_path = "media/"
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        uuid_filename = self.unique_filename(filename=self.file_name)
        video_path = os.path.join(save_path, uuid_filename)
        self.video_file.save(video_path)
