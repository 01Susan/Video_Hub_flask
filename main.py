from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
import uuid
import cv2
import datetime
import tempfile

# initializing the flask instance
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1GB
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(250), nullable=False)
    upload_date = db.Column(db.Date, nullable=False)
    video_path = db.Column(db.String(255), nullable=False)


# db.create_all()


@app.route('/')
def home():
    return "Welcome to Video Hub"


@app.route('/upload', methods=['POST'])
def upload():
    """route to upload your video"""
    video_file = request.files['video']
    file_name = video_file.filename
    temp_file(video_file)

    # Validating the video file extension
    allowed_extensions = ('.mp4', '.mkv')
    if not file_name.endswith(allowed_extensions):
        return jsonify({
            "error": f"Invalid file format.",
            "allowed_format": allowed_extensions
        }), 400

    # Read the file data and calculating the file size
    file_data = video_file.read()
    file_size = len(file_data)
    if file_size > (1 * (1024 ** 3)):  # Check if the file size is greater than 1 GB
        return jsonify({"error": "File size exceeds 1 GB."})

    # Save the video file to a desired location
    save_path = "media/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    uuid_filename = unique_filename(filename=file_name)
    video_path = os.path.join(save_path, uuid_filename)
    video_file.save(video_path)

    # save in database
    new_video = Videos(
        video_name=file_name,
        upload_date=date.today(),
        video_path=video_path
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify(response={"success": "Successfully uploaded the video"})


def unique_filename(filename):
    extension = filename.split('.')[-1]
    return f"{uuid.uuid4().hex}.{extension}"


def get_video_duration(file_path):
    # create video capture object
    data = cv2.VideoCapture(file_path)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f"duration in seconds: {seconds}")
    print(f"video time: {video_time}")


def temp_file(file):
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)

    try:
        # Save the uploaded file to the temporary file
        file.save(temp_file.name)

        # Here, you can process the temporary file as needed
        # For example, you can move it to a permanent location, process it, etc.
        get_video_duration(temp_file.name)
        # For demonstration purposes, let's print the temporary file's path

        # Rest of your code to handle the uploaded file

    finally:
        # Close and delete the temporary file
        temp_file.close()
        os.remove(temp_file.name)


def check_file_size(file_size_in_bytes):
    file_size_mb = file_size_in_bytes / (1024 ** 2)
    file_size_gb = file_size_in_bytes / (1024 ** 3)


if __name__ == '__main__':
    app.run(debug=True)
