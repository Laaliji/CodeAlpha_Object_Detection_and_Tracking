from flask import Flask, request, jsonify
from functools import wraps
import torch
from PIL import Image
import io
import logging
import os
import cv2  # OpenCV to process video frames
import numpy as np
from torchvision import transforms
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_model():
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', 
                               path='model/best.pt', 
                               force_reload=True)
        model.eval()
        return model
    except Exception as e:
        logger.error(f"Failed to load YOLO model: {str(e)}")
        raise RuntimeError(f"Model loading failed: {str(e)}")

# Load YOLO model
model = load_model()

# Constants
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov'}  # Allow video formats
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB size limit

def allowed_file(filename):
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS

def validate_video(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'video' not in request.files:
            return jsonify({'error': 'No video uploaded'}), 400

        file = request.files['video']

        if not file or not file.filename:
            return jsonify({'error': 'Empty file submitted'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Only MP4, AVI, MOV allowed'}), 400

        # Check video size
        file.seek(0, 2)  # Seek to the end of the file
        size = file.tell()
        file.seek(0)  # Reset file pointer
        if size > MAX_VIDEO_SIZE:
            return jsonify({'error': 'File too large. Maximum size is 100MB'}), 400

        return f(*args, **kwargs)
    return decorated_function

@app.route('/detect-video', methods=['POST'])
@validate_video
def detect_video():
    try:
        file = request.files['video']
        video_bytes = file.read()
        
        # Open video using OpenCV
        video_stream = cv2.VideoCapture(io.BytesIO(video_bytes))

        if not video_stream.isOpened():
            return jsonify({'error': 'Could not read video'}), 400

        frame_results = []

        while True:
            ret, frame = video_stream.read()
            if not ret:
                break  # End of video

            # Convert frame from BGR (OpenCV format) to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            # Apply transformations
            image_tensor = transforms.ToTensor()(pil_image).unsqueeze(0)

            # Perform detection
            with torch.no_grad():
                results = model(image_tensor)

            # Collect detections
            detections = results.xyxy[0]  # xyxy format detections

            frame_detection = [{
                'x1': float(d[0]),
                'y1': float(d[1]),
                'x2': float(d[2]),
                'y2': float(d[3]),
                'confidence': float(d[4]),
                'class': int(d[5])
            } for d in detections.tolist()]

            frame_results.append(frame_detection)

        video_stream.release()  # Release the video stream

        return jsonify({
            'message': 'Video processed successfully',
            'frame_detections': frame_results
        }), 200

    except torch.cuda.OutOfMemoryError:
        logger.error("CUDA out of memory error")
        torch.cuda.empty_cache()
        return jsonify({'error': 'Server is currently overloaded'}), 503

    except Exception as e:
        logger.error(f"Error during video processing: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
