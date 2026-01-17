# CV-Traffic: Application of Computer Vision in Estimating Traffic Density for Automatic Signal Timing Setting

A single-page web application for estimating traffic density from uploaded videos and recommending signal timing.

## Features
- Upload MP4 traffic videos
- Extract frames and detect vehicles using YOLOv8
- Estimate traffic density (Low/Medium/High)
- Compute recommended green signal time
- Display results with processed frame and optional plot

## Tech Stack
- Python
- Streamlit
- OpenCV
- YOLOv8 (via ultralytics)
- NumPy, Matplotlib

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Usage
1. Upload a traffic video (MP4)
2. Click "Process Video"
3. View results: vehicle count, density, signal time, processed frame

## Project Structure
- `app.py`: Main Streamlit application
- `video_processing.py`: Video frame extraction
- `vehicle_detection.py`: Vehicle detection using YOLO
- `signal_timing.py`: Density estimation and signal timing logic
- `requirements.txt`: Python dependencies
