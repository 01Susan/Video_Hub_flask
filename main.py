import os
from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from utils import save_as_temp_file, save_original_file, get_search_result, video_charge
from video_validation import VideoValidation

# initializing the flask instance
app = Flask(__name__)
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
HOST_NAME = os.getenv('HOST_NAME')

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST_NAME}/{DATABASE_NAME}'

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()


# Base.metadata.create_all(engine)


@app.route('/')
def home():
    return "Welcome to Video Hub"


@app.route('/upload', methods=['POST'])
def upload():
    """Uploads and validates a video file. Returns success or error messages."""
    video_file = request.files['video']
    if not video_file:
        return jsonify({"error": "please provide a video file"}), 400
    tmp_file_path = save_as_temp_file(video_file)
    video_validation = VideoValidation(tmp_file_path=tmp_file_path)

    # Validating the video file extension
    if not video_validation.is_validate_extensions():
        os.remove(tmp_file_path)
        return jsonify({
            "error": f"Invalid file format.",
            "allowed_format": video_validation.allowed_extensions
        }), 400

    if video_validation.get_file_size() > 1:
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


@app.route('/upload-date', methods=['GET'])
def get_video_by_upload_date():
    """Get video info by upload date search. Expects 'date' parameter (YYYY-MM-DD format)."""
    uploaded_date_str = request.args.get("date")
    try:
        parsed_date = datetime.strptime(uploaded_date_str, '%Y-%m-%d').date()
    except ValueError as e:
        return jsonify({'error': str(e)})
    search_result = get_search_result(search_string=parsed_date, session=session)
    if len(search_result) == 0:
        return jsonify({"message": f"No videos found with the given {uploaded_date_str}"}), 404
    return jsonify(video_info=search_result), 200


@app.route('/video-name', methods=['GET'])
def get_video_by_name():
    """Get video info by name search. Expects 'name' parameter in the request."""
    video_name = request.args.get("name")
    search_result = get_search_result(search_string=video_name, session=session)
    if len(search_result) == 0:
        return jsonify({"message": f"No videos found with the given {video_name}"}), 404
    return jsonify(video_info=search_result), 200


@app.route('/price-info', methods=['GET', 'POST'])
def get_price_info():
    """Calculate and return video price info based on user input like size, duration, and type."""
    video_size = int(request.args.get("size-in-mb"))  # size in mb
    video_duration = int(request.args.get("duration-in-sec"))  # duration in sec
    video_type = request.args.get("type").lower()
    allowed_extensions = ['mp4', 'mkv']
    if video_type not in allowed_extensions:
        return jsonify({
            "error": f"{video_type} type is not supported",
            "type": f"{allowed_extensions} are only supported type"
        })

    charge = video_charge(video_size=video_size, video_duration=video_duration)

    return jsonify(price_info={
        "price": f"${charge}"
    }), 200


@app.route("/video_info&charge", methods=["POST"])
def get_video_all_info():
    """Calculate and return various video information along with the charge based on the uploaded video."""
    video_file = request.files['video']
    if not video_file:
        return jsonify({"error": "please provide a video file"}), 400
    tmp_file_path = save_as_temp_file(video_file)
    video_validation = VideoValidation(tmp_file_path=tmp_file_path)
    video_duration = int(video_validation.get_file_duration())
    video_validation.get_file_size()
    video_in_mb = video_validation.file_size_in_mb

    charge = 0
    if video_validation.is_validate_extensions():
        charge += video_charge(video_size=video_in_mb, video_duration=video_duration)
    os.remove(tmp_file_path)
    return jsonify(video_info={
        "video_name": video_validation.file_name,
        "video_type": video_validation.video_type,
        "type_supported": video_validation.is_validate_extensions(),
        "video_duration": f"{round(video_duration / 60, 2)} minutes",
        "video_size": f"{round(video_in_mb, 2)} MB",
        "video_charge": f"${charge}"
    })


if __name__ == '__main__':
    app.run(debug=True)
