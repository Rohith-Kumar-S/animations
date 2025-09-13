import streamlit as st
import numpy as np
import cv2
import time
from queue import Queue
from threading import Thread
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from av import VideoFrame

st.title("Server-generated Dummy Frames via WebRTC")

# --------------------------------------------------------------------
# 1️⃣  Frame producer: generates dummy frames and puts them in a queue
# --------------------------------------------------------------------
frame_queue: "Queue[np.ndarray]" = Queue(maxsize=1)  # keep only latest frame

def producer():
    """Generate synthetic frames and push to queue."""
    i = 0
    while True:
        # Create a dummy RGB image with moving color
        img = np.zeros((240, 320, 3), dtype=np.uint8)
        color = ((i * 5) % 255, (i * 3) % 255, (i * 7) % 255)
        cv2.putText(img, f"Frame {i}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
        
        # Clear queue and add new frame
        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except:
                pass
        frame_queue.put(img)
        
        i += 1
        time.sleep(1/15)  # ~15 FPS

Thread(target=producer, daemon=True).start()

# --------------------------------------------------------------------
# 2️⃣  WebRTC processor: pulls latest frame from queue for streaming
# --------------------------------------------------------------------
class DummyVideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        """
        Instead of using the incoming browser frame,
        return the latest server-generated frame.
        """
        # Get the latest frame from queue
        if not frame_queue.empty():
            img = frame_queue.get()
        else:
            # If queue is empty, send a black frame
            img = np.zeros((240, 320, 3), dtype=np.uint8)
        
        # Convert numpy array to VideoFrame
        return VideoFrame.from_ndarray(img, format="bgr24")

# --------------------------------------------------------------------
# 3️⃣  WebRTC streamer: sends our frames to the browser
# --------------------------------------------------------------------
webrtc_ctx = webrtc_streamer(
    key="dummy-stream",
    video_processor_factory=DummyVideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    sendback_audio=False,
    rtc_configuration={  # Optional: Add STUN servers for better connectivity
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)