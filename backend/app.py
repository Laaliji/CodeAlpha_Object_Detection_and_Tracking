import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('model/best.pt')  

# Load the image
image_path = 'C:/Users/hp/Documents/Task3_CodeAlpha/frontend/public/u.jpg'  # Update this with your image path
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load image.")
    exit()

# Perform inference on the image
results = model(image)

# Get the annotated image
annotated_image = results[0].plot()

# Display the annotated image
cv2.imshow('YOLOv8 Image Detection', annotated_image)

# Wait until a key is pressed
cv2.waitKey(0)

# Release resources
cv2.destroyAllWindows()
