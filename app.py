import streamlit as st
import cv2
import numpy as np
st.title("Live Webcam Feed")
if "stop" not in st.session_state:
    st.session_state["stop"] = False
if "start" not in st.session_state:
    st.session_state["start"] = True

# Create a placeholder for the video frames
frame_window = st.empty()
if st.button("Stop"):
    st.session_state["stop"] = True
if st.button("Start"):
    st.session_state["start"] = True
    st.session_state["stop"] = False
# Open default webcam (use a file path or URL for other sources)
if st.session_state["start"]:
    cap = cv2.VideoCapture(0)
    # Loop until user stops the app
    while True:
        if st.session_state["stop"]:
            cap.release()
            break
        ret, frame  = cap.read()
        if not ret:
            st.write("Failed to grab frame")
            break

        # Convert BGR (OpenCV default) to RGB for correct colors
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the Streamlit app
        frame_window.image(frame, channels="RGB")
    

