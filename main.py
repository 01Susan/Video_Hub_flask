import os

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils import save_as_temp_file, save_original_file
from video_validation import VideoValidation

# initializing the flask instance
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1GB

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://susan:password@localhost/videohub'
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()


# Base.metadata.create_all(engine)


@app.route('/')
def home():
    return "Welcome to Video Hub"


@app.route('/upload', methods=['POST'])
def upload():
    video_file = request.files['video']
    tmp_file_path = save_as_temp_file(video_file)
    video_validation = VideoValidation(tmp_file_path=tmp_file_path)
    """route to upload your video"""

    # Validating the video file extension
    if not video_validation.is_validate_extensions():
        os.remove(tmp_file_path)
        return jsonify({
            "error": f"Invalid file format.",
            "allowed_format": video_validation.allowed_extensions
        }), 400

    if video_validation.get_file_size() > 0.3:
        os.remove(tmp_file_path)
        return jsonify({
            "error": "File size greater than 1GB"
        })

    if video_validation.get_file_duration() > 600:
        os.remove(tmp_file_path)
        return jsonify({
            "error": f"File duration greater than 10 min"
        })

    save_original_file(tmp_file_path, video_validation, session)

    return jsonify(response={"success": "Successfully uploaded the video"})


if __name__ == '__main__':
    app.run(debug=True)
