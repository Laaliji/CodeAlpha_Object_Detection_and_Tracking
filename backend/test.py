import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('C:/Users/hp/Documents/Task3_CodeAlpha/backend/model/best.pt')

# Open the video file or webcam
video_path = 'C:/Users/hp/Documents/Task3_CodeAlpha/frontend/public/video.mp4'
cap = cv2.VideoCapture(video_path)

# Set a lower resolution for faster processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading frame.")
        break

    # Resize frame for faster inference (optional)
    resized_frame = cv2.resize(frame, (640, 480))

    # Perform inference with faster settings
    results = model.predict(resized_frame, imgsz=640, conf=0.5, iou=0.5, verbose=False)

    # Get the annotated frame
    annotated_frame = results[0].plot()

    # Display the frame with detections
    cv2.imshow('YOLOv8 Optimized Video Detection', annotated_frame)

    # Press 'q' to quit the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()