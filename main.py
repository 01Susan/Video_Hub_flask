import hashlib
from moviepy.editor import VideoFileClip
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
import uuid

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
    print(type(file_name))
    print(file_name)
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

    # Check the file duration
    print("file duration:", get_video_duration(video_file))

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
    hex_string = hashlib.md5(filename.encode("UTF-8")).hexdigest()
    print("hash file_name", hex_string)
    print("unique id", uuid.UUID(hex=hex_string))
    return str(uuid.UUID(hex=hex_string))


def get_video_duration(file):
    try:
        file.seek(0)
        video = VideoFileClip(file)
        duration = video.duration
        video.close()
        return str(duration)
    except Exception as e:
        print(f"Error: {e}")
        return None


def check_file_size(file_size_in_bytes):
    file_size_mb = file_size_in_bytes / (1024 ** 2)
    file_size_gb = file_size_in_bytes / (1024 ** 3)


if __name__ == '__main__':
    app.run(debug=True)
