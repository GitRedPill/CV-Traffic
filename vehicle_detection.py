import cv2
import numpy as np

# Create background subtractor
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

def detect_vehicles(frame_path):
    """
    Detect vehicles using background subtraction.
    Returns count of vehicles and annotated frame.
    """
    frame = cv2.imread(frame_path)
    if frame is None:
        return 0, None

    # Apply background subtraction
    fg_mask = subtractor.apply(frame)

    # Clean up the mask
    kernel = np.ones((5,5), np.uint8)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    vehicle_count = 0
    annotated_frame = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Minimum area for vehicle
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            vehicle_count += 1

    return vehicle_count, annotated_frame