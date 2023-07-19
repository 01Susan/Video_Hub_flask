from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import uuid
import cv2
import datetime
import tempfile

# initializing the flask instance
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1GB

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://susan:password@localhost/videohub'
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()


class Video(Base):
    __tablename__ = 'videos'
    video_id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String(255), nullable=False)
    video_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(engine)


@app.route('/')
def home():
    return "Welcome to Video Hub"


@app.route('/upload', methods=['POST'])
def upload():
    """route to upload your video"""
    video_file = request.files['video']
    file_name = video_file.filename
    file_path = temp_file(video_file)
    print(file_path)
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

    # Validate the video duration

    video_duration = get_video_duration(file_path)
    print(video_duration)

    if video_duration > 600:
        return jsonify({
            "error": f"Video duration exceeds 10 min."
        })

    # Save the video file to a desired location
    save_path = "media/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    uuid_filename = unique_filename(filename=file_name)
    video_path = os.path.join(save_path, uuid_filename)
    video_file.save(video_path)

    # save in database
    new_video = Video(
        video_name=file_name,
        video_path=video_path
    )
    session.add(new_video)
    session.commit()

    return jsonify(response={"success": "Successfully uploaded the video"})


def unique_filename(filename):
    extension = filename.split('.')[-1]
    return f"{uuid.uuid4().hex}.{extension}"


def get_video_duration(file_path):
    # create video capture object
    try:
        # create video capture object
        print("get_video", file_path)
        data = cv2.VideoCapture(file_path)

        if not data.isOpened():
            raise ValueError("Failed to open the video file.")

        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Number of frames:", frames)

        fps = data.get(cv2.CAP_PROP_FPS)
        print("Frames per second (FPS):", fps)

        # calculate duration of the video
        seconds = round(frames / fps)

        return seconds
    except Exception as e:
        print("Error:", e)
        return None


def temp_file(file):
    # Create a temporary file
    new_directory_path = os.path.join("media/", 'temp/')
    if not os.path.exists(new_directory_path):
        os.mkdir(new_directory_path)
    save_path = os.path.join(new_directory_path, file.filename)
    file.save(save_path)
    # Here, you can process the temporary file as needed
    return save_path


if __name__ == '__main__':
    app.run(debug=True)
