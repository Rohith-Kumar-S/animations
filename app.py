import streamlit as st
import cv2
import numpy as np
st.title("Live Webcam Feed")

# Create a placeholder for the video frames
# frame_window = st.empty()

# Open default webcam (use a file path or URL for other sources)
enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

# Loop until user stops the app
if enable and picture is not None:
    bytes_data = picture.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Convert BGR (OpenCV default) to RGB for correct colors
    frame = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Display the frame in the Streamlit app
    st.image(frame, channels="RGB")
