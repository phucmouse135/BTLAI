import os
import cv2
import numpy as np
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_camera(camera_id=0, width=640, height=480):
    """
    Initialize the camera with specified parameters
    
    Args:
        camera_id: Camera device ID (default: 0 for primary webcam)
        width: Desired frame width
        height: Desired frame height
        
    Returns:
        OpenCV VideoCapture object or None if initialization failed
    """
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        logger.error(f"Failed to open camera with ID {camera_id}")
        return None
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    logger.info(f"Camera initialized with resolution {width}x{height}")
    return cap

def annotate_frame(frame, results, ear_threshold=0.2):
    """
    Add annotations to the frame based on detection results
    
    Args:
        frame: Input video frame
        results: Detection results from the model
        ear_threshold: Eye aspect ratio threshold for drowsiness
        
    Returns:
        Annotated frame
    """
    # Create a copy of the frame for annotations
    annotated_frame = frame.copy()
    
    # Get frame dimensions
    h, w = frame.shape[:2]
    
    # Add status box at the top
    status_height = 70
    cv2.rectangle(annotated_frame, (0, 0), (w, status_height), (0, 0, 0), -1)
    
    # Display overall status
    if results.get("drowsy", False):
        status_text = "DROWSY"
        status_color = (0, 0, 255)  # Red
    elif results.get("distracted", False):
        status_text = "DISTRACTED"
        status_color = (0, 165, 255)  # Orange
    else:
        status_text = "ALERT"
        status_color = (0, 255, 0)  # Green
        
    cv2.putText(annotated_frame, status_text, (int(w/2) - 50, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    
    # Display metrics
    # EAR - Eye Aspect Ratio
    ear = results.get("eye_aspect_ratio", 0)
    ear_color = (0, 0, 255) if ear < ear_threshold else (0, 255, 0)
    cv2.putText(annotated_frame, f"EAR: {ear:.2f}", (10, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, ear_color, 2)
    
    # Head direction
    head_dir = results.get("head_direction", "unknown")
    head_color = (0, 255, 0) if head_dir == "forward" else (0, 165, 255)
    cv2.putText(annotated_frame, f"Head: {head_dir}", (10, 130), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, head_color, 2)
    
    # Hand position
    hand_pos = results.get("hand_position", "unknown")
    hand_color = (0, 255, 0) if hand_pos == "hands_on_wheel" else (0, 165, 255)
    cv2.putText(annotated_frame, f"Hands: {hand_pos}", (10, 160), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2)
    
    # Confidence
    conf = results.get("confidence", 0) * 100
    cv2.putText(annotated_frame, f"Confidence: {conf:.1f}%", (10, 190), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return annotated_frame

def calculate_fps():
    """Simple FPS calculator with moving average"""
    class FPSCounter:
        def __init__(self, window_size=30):
            self.frame_times = []
            self.window_size = window_size
            self.last_time = time.time()
            self.start_time = time.time()
            
        def update(self):
            current_time = time.time()
            delta = current_time - self.last_time
            self.last_time = current_time
            
            self.frame_times.append(delta)
            
            # Keep only the most recent frames
            if len(self.frame_times) > self.window_size:
                self.frame_times.pop(0)
                
        def get_fps(self):
            if not self.frame_times:
                return 0
                
            avg_time = sum(self.frame_times) / len(self.frame_times)
            return 1.0 / avg_time if avg_time > 0 else 0
        
        def get_elapsed_time(self):
            """Return the time elapsed since starting the counter in seconds"""
            return time.time() - self.start_time
            
    return FPSCounter()

def save_config(config, filepath):
    """Save configuration to a file"""
    import json
    
    try:
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info(f"Configuration saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        return False
        
def load_config(filepath):
    """Load configuration from a file"""
    import json
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {filepath}")
            return config
        else:
            logger.warning(f"Configuration file {filepath} not found")
            return {}
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return {}