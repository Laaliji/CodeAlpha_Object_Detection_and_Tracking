import cv2
from ultralytics import YOLO

model = YOLO('model/best(2).pt')  

image_path = 'C:/Users/hp/Documents/Task3_CodeAlpha/frontend/public/test.jpg' 
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image.")
    exit()

results = model(image)

annotated_image = results[0].plot()

cv2.imshow('YOLOv8 Image Detection', annotated_image)

cv2.waitKey(0)

cv2.destroyAllWindows()
