from ultralytics import YOLO
import cv2

# Load YOLO model (YOLOv8n is lightweight)
model = YOLO('yolov8n.pt')  # Will download if not present

def detect_vehicles(frame_path):
    """
    Detect vehicles in a frame using YOLO.
    Returns count of vehicles and annotated frame.
    Vehicles: car, truck, bus, motorbike.
    """
    frame = cv2.imread(frame_path)
    results = model(frame, classes=[2, 3, 5, 7])  # COCO classes: 2=car, 3=motorcycle, 5=bus, 7=truck

    vehicle_count = len(results[0].boxes) if results[0].boxes else 0

    # Annotate frame
    annotated_frame = results[0].plot()

    return vehicle_count, annotated_frame