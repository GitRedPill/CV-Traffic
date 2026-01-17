import cv2
import os

def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extract frames from video at specified frame rate (frames per second).
    Saves frames as images in output_dir.
    Returns list of frame paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frame_rate) if frame_rate > 0 else 1

    frame_paths = []
    frame_count = 0
    success, frame = cap.read()
    while success:
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
        success, frame = cap.read()
        frame_count += 1

    cap.release()
    return frame_paths