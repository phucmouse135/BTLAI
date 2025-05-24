import os
import cv2
import numpy as np
import time
import logging
import json

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
    annotated = frame.copy()
    
    # Draw status box
    status_color = (0, 255, 0)  # Green by default (OK)
    status_text = "Status: OK"
    
    if results.get('face_detected', False) == False:
        status_color = (0, 0, 255)  # Red
        status_text = "Status: No Face Detected"
    elif results.get('drowsy', False):
        status_color = (0, 0, 255)  # Red
        status_text = "Status: DROWSY!"
    elif results.get('distracted', False):
        status_color = (0, 165, 255)  # Orange
        status_text = "Status: DISTRACTED!"
    
    # Add status box
    cv2.rectangle(annotated, (10, 10), (300, 100), (0, 0, 0), -1)
    cv2.putText(annotated, status_text, (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    
    # Add EAR information if available
    if 'ear' in results:
        ear_text = f"EAR: {results['ear']:.2f}/{ear_threshold:.2f}"
        ear_color = (0, 255, 0) if results['ear'] >= ear_threshold else (0, 0, 255)
        cv2.putText(annotated, ear_text, (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, ear_color, 2)
    
    # Add head position if available
    if 'head_position' in results:
        head_text = f"Head: {results['head_position']}"
        cv2.putText(annotated, head_text, (20, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Add hand position if available
    if 'hand_position' in results:
        hand_text = f"Hands: {results['hand_position']}"
        hand_color = (0, 255, 0) if results['hand_position'] == 'on_wheel' else (0, 165, 255)
        cv2.putText(annotated, hand_text, (150, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 1)
    
    return annotated

def calculate_fps(prev_time=None):
    """
    Calculate and return FPS based on previous time
    
    Args:
        prev_time: Previous time measurement
        
    Returns:
        Tuple of (fps, current_time)
    """
    curr_time = time.time()
    fps = 0
    
    if prev_time:
        fps = 1 / (curr_time - prev_time)
    
    return fps, curr_time

def save_config(config_path, config_data):
    """
    Save configuration data to a JSON file
    
    Args:
        config_path: Path to save the config file
        config_data: Dictionary of configuration parameters
    """
    try:
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        logger.info(f"Configuration saved to {config_path}")
    except Exception as e:
        logger.error(f"Failed to save configuration: {str(e)}")

def load_config(config_path):
    """
    Load configuration data from a JSON file
    
    Args:
        config_path: Path to the config file
        
    Returns:
        Dictionary of configuration parameters or empty dict if file not found
    """
    if not os.path.exists(config_path):
        logger.warning(f"Configuration file {config_path} not found, using defaults")
        return {}
    
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config_data
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        return {}
