import os
os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'
import streamlit as st
import tempfile
import os
from video_processing import extract_frames
from vehicle_detection import detect_vehicles
from signal_timing import estimate_density, compute_signal_time
import matplotlib.pyplot as plt
import json
import subprocess
from datetime import datetime

st.title("Traffic Density Estimator for Signal Timing")

uploaded_file = st.file_uploader("Upload a traffic video (MP4)", type=["mp4"])

if uploaded_file is not None:
    if st.button("Process Video"):
        with st.spinner("Processing..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                video_path = tmp_file.name

            # Extract frames
            temp_dir = tempfile.mkdtemp()
            frame_paths = extract_frames(video_path, temp_dir, frame_rate=1)  # 1 fps

            # Detect vehicles in each frame
            vehicle_counts = []
            annotated_frames = []
            for path in frame_paths:
                count, annotated = detect_vehicles(path)
                vehicle_counts.append(count)
                annotated_frames.append(annotated)

            # Estimate density
            density, avg_count = estimate_density(vehicle_counts)
            signal_time = compute_signal_time(density)

            # Display results
            st.subheader("Results")
            st.write(f"Total Frames Processed: {len(frame_paths)}")
            st.write(f"Average Vehicle Count: {avg_count:.2f}")
            st.write(f"Traffic Density: {density}")
            st.write(f"Recommended Green Signal Time: {signal_time} seconds")

            # Show one processed frame
            if annotated_frames:
                st.image(annotated_frames[0], caption="Processed Frame with Detections", use_column_width=True)

            # Optional plot
            if vehicle_counts:
                fig, ax = plt.subplots()
                ax.plot(vehicle_counts)
                ax.set_xlabel("Frame")
                ax.set_ylabel("Vehicle Count")
                ax.set_title("Vehicle Count Over Time")
                st.pyplot(fig)

            # Save results to data
            results_file = 'data/results.json'
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []

            new_result = {
                'timestamp': datetime.now().isoformat(),
                'frames_processed': len(frame_paths),
                'avg_vehicle_count': avg_count,
                'density': density,
                'signal_time': signal_time
            }
            data.append(new_result)

            with open(results_file, 'w') as f:
                json.dump(data, f, indent=4)

            # Commit to GitHub
            try:
                subprocess.run(['git', 'add', 'data/'], check=True)
                subprocess.run(['git', 'commit', '-m', f'Add analysis result: {density} density, {signal_time}s signal time'], check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                st.success("Results saved and committed to GitHub!")
            except subprocess.CalledProcessError as e:
                st.error(f"Failed to commit to GitHub: {e}")

            # Cleanup
            os.unlink(video_path)
            for path in frame_paths:
                os.unlink(path)
            os.rmdir(temp_dir)