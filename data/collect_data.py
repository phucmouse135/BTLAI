import os
import cv2
import numpy as np
import time
import argparse
from datetime import datetime
import mediapipe as mp
import json

def create_directory_structure(base_dir):
    """Create the directory structure for data collection"""
    # Create main data directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)
    
    # Create class directories for general classification
    general_classes = ['focused', 'distracted']
    for class_name in general_classes:
        os.makedirs(os.path.join(base_dir, class_name), exist_ok=True)
    
    # Create specific subdirectories for detailed data collection
    detailed_classes = {
        'eye_state': ['eyes_open', 'eyes_half_closed', 'eyes_closed'],
        'head_position': ['head_forward', 'head_tilted', 'head_sideways'],
        'hand_position': ['hands_on_wheel', 'hands_off_wheel', 'holding_object']
    }
    
    for category, subclasses in detailed_classes.items():
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for subclass in subclasses:
            os.makedirs(os.path.join(category_dir, subclass), exist_ok=True)
    
    print(f"Created directory structure at {base_dir}")

def analyze_face_metrics(frame):
    """
    Analyze face to extract metrics like eye openness and head position
    
    Returns:
        dict: Metrics including eye_aspect_ratio and head_position
    """
    # Initialize MediaPipe face mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Process the frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    metrics = {
        "eye_aspect_ratio": None,
        "head_position": "unknown"
    }
    
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        
        # Eye landmark indices
        LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        
        # Extract eye landmarks
        h, w = frame.shape[:2]
        
        # Calculate eye aspect ratio (EAR)
        def calculate_ear(eye_indices):
            points = []
            for idx in eye_indices:
                landmark = landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                points.append((x, y))
            
            # Compute the euclidean distances
            A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
            B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
            C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
            
            # Calculate EAR
            ear = (A + B) / (2.0 * C) if C > 0 else 0
            return ear
        
        left_ear = calculate_ear(LEFT_EYE_INDICES)
        right_ear = calculate_ear(RIGHT_EYE_INDICES)
        avg_ear = (left_ear + right_ear) / 2.0
        metrics["eye_aspect_ratio"] = avg_ear
        
        # Determine eye state
        if avg_ear < 0.15:
            metrics["eye_state"] = "eyes_closed"
        elif avg_ear < 0.25:
            metrics["eye_state"] = "eyes_half_closed"
        else:
            metrics["eye_state"] = "eyes_open"
        
        # Estimate head position
        # Get nose tip position
        nose_tip = landmarks.landmark[4]
        nose_x, nose_y = nose_tip.x, nose_tip.y
        
        # Check if head is turned left/right
        center_offset_x = abs(nose_x - 0.5) / 0.5
        
        if center_offset_x > 0.2:
            metrics["head_position"] = "head_sideways"
        else:
            # Check vertical tilt using relative positions of landmarks
            forehead = landmarks.landmark[10]  # Forehead point
            chin = landmarks.landmark[152]     # Chin point
            
            if abs(forehead.y - chin.y) < 0.25:  # Reduced vertical distance indicates tilt
                metrics["head_position"] = "head_tilted"
            else:
                metrics["head_position"] = "head_forward"
    
    # Clean up
    face_mesh.close()
    
    return metrics

def analyze_hand_position(frame):
    """
    Analyze hand position to determine wheel-holding state
    
    Returns:
        str: hand position classification
    """
    # Initialize MediaPipe hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Process the frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    hand_state = "hands_off_wheel"  # Default
    
    if results.multi_hand_landmarks:
        h, w = frame.shape[:2]
        
        # Define wheel region (bottom center of frame)
        wheel_region_x = (w * 0.3, w * 0.7)  # 30-70% of width
        wheel_region_y = (h * 0.6, h * 0.9)  # 60-90% of height
        
        # Check hand positions
        for hand_landmarks in results.multi_hand_landmarks:
            # Use wrist as reference point
            wrist = hand_landmarks.landmark[0]
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            
            # Check if holding something (fingers in gripping position)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            distance = np.sqrt(
                (thumb_tip.x - index_tip.x)**2 + 
                (thumb_tip.y - index_tip.y)**2
            )
            
            is_gripping = distance < 0.1  # Close fingers indicate gripping
            
            if (wheel_region_x[0] <= wrist_x <= wheel_region_x[1] and 
                wheel_region_y[0] <= wrist_y <= wheel_region_y[1]):
                hand_state = "hands_on_wheel"
            elif is_gripping:
                hand_state = "holding_object"
                break
    
    # Clean up
    hands.close()
    
    return hand_state

def collect_data(output_dir, class_name, num_samples=200, delay=0.2, collect_detailed=True):
    """
    Collect image data using webcam with detailed metrics
    
    Args:
        output_dir: Directory to save images
        class_name: Primary class of images being collected (focused/distracted)
        num_samples: Number of samples to collect
        delay: Delay between captures (seconds)
        collect_detailed: Whether to collect detailed subclass data
    """
    # Validate class name
    valid_classes = ['focused', 'distracted']
    if class_name not in valid_classes and class_name not in [
        'eyes_open', 'eyes_half_closed', 'eyes_closed',
        'head_forward', 'head_tilted', 'head_sideways',
        'hands_on_wheel', 'hands_off_wheel', 'holding_object'
    ]:
        raise ValueError(f"Class name must be one of: {', '.join(valid_classes)} or a valid subclass")
    
    # Determine the collection mode (general or specific subclass)
    if class_name in valid_classes:
        # General collection mode
        collection_mode = "general"
        class_dir = os.path.join(output_dir, class_name)
    else:
        # Specific feature collection mode
        collection_mode = "specific"
        
        # Determine which category this subclass belongs to
        if class_name in ['eyes_open', 'eyes_half_closed', 'eyes_closed']:
            category = 'eye_state'
        elif class_name in ['head_forward', 'head_tilted', 'head_sideways']:
            category = 'head_position'
        else:
            category = 'hand_position'
            
        class_dir = os.path.join(output_dir, category, class_name)
    
    # Ensure output directory exists
    os.makedirs(class_dir, exist_ok=True)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print(f"Collecting {num_samples} samples for class '{class_name}'")
    print("Press 's' to start/pause collection, 'q' to quit")
    
    # Collection variables
    collecting = False
    count = 0
    last_capture_time = 0
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Create a copy for display with status information
        display_frame = frame.copy()
        
        # Add status text
        status = "COLLECTING" if collecting else "PAUSED"
        cv2.putText(display_frame, f"Status: {status}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display_frame, f"Class: {class_name}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display_frame, f"Captured: {count}/{num_samples}", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # If collecting or about to start, analyze the frame
        if collecting or (count == 0 and not collecting):
            # Extract metrics for annotation
            face_metrics = analyze_face_metrics(frame)
            hand_state = analyze_hand_position(frame)
            
            # Display metrics on frame
            ear = face_metrics.get("eye_aspect_ratio", 0)
            eye_state = face_metrics.get("eye_state", "unknown")
            head_pos = face_metrics.get("head_position", "unknown")
            
            # Make sure ear is not None before formatting
            ear_value = 0.0 if ear is None else ear
            
            cv2.putText(display_frame, f"EAR: {ear_value:.2f}", (10, 120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Eyes: {eye_state}", (10, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Head: {head_pos}", (10, 180), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Hands: {hand_state}", (10, 210), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Data Collection', display_frame)
        
        # Capture logic
        current_time = time.time()
        if collecting and current_time - last_capture_time >= delay and count < num_samples:
            # For specific collection mode, ensure the current frame matches the target class
            if collection_mode == "specific":
                if (
                    (category == 'eye_state' and face_metrics.get("eye_state") != class_name) or
                    (category == 'head_position' and face_metrics.get("head_position") != class_name) or
                    (category == 'hand_position' and hand_state != class_name)
                ):
                    # Skip this frame as it doesn't match the target class
                    # Don't update last_capture_time to allow immediate retry with next frame
                    cv2.putText(display_frame, "WAITING FOR CORRECT POSE", (int(frame.shape[1]/2) - 150, 240), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.imshow('Data Collection', display_frame)
                    continue
            
            # Generate filename with timestamp to ensure uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{class_name}_{timestamp}_{count}.jpg"
            filepath = os.path.join(class_dir, filename)
            
            # Save image
            cv2.imwrite(filepath, frame)
            
            # If collecting detailed data, also save to appropriate subfolders
            if collect_detailed and collection_mode == "general":
                # Save to eye state folder
                eye_state = face_metrics.get("eye_state", "unknown")
                if eye_state != "unknown":
                    eye_dir = os.path.join(output_dir, "eye_state", eye_state)
                    eye_filepath = os.path.join(eye_dir, filename)
                    cv2.imwrite(eye_filepath, frame)
                
                # Save to head position folder
                head_pos = face_metrics.get("head_position", "unknown")
                if head_pos != "unknown":
                    head_dir = os.path.join(output_dir, "head_position", head_pos)
                    head_filepath = os.path.join(head_dir, filename)
                    cv2.imwrite(head_filepath, frame)
                
                # Save to hand position folder
                if hand_state != "unknown":
                    hand_dir = os.path.join(output_dir, "hand_position", hand_state)
                    hand_filepath = os.path.join(hand_dir, filename)
                    cv2.imwrite(hand_filepath, frame)
                
                # Save metadata alongside the image
                metadata = {
                    "filename": filename,
                    "class": class_name,
                    "eye_aspect_ratio": face_metrics.get("eye_aspect_ratio"),
                    "eye_state": eye_state,
                    "head_position": head_pos,
                    "hand_position": hand_state,
                    "timestamp": timestamp
                }
                
                metadata_filepath = os.path.join(class_dir, f"{os.path.splitext(filename)[0]}.json")
                with open(metadata_filepath, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            count += 1
            last_capture_time = current_time
            
            print(f"Captured image {count}/{num_samples}")
        
        # Check if collection is complete
        if count >= num_samples:
            print(f"Collection complete for class '{class_name}'")
            break
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        # 's' to start/pause collection
        if key == ord('s'):
            collecting = not collecting
            print(f"Collection {'started' if collecting else 'paused'}")
        
        # 'q' to quit
        elif key == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Collect training data for driver monitoring')
    parser.add_argument('--dir', type=str, default='../data', 
                       help='Directory to save collected data')
    parser.add_argument('--class', dest='class_name', type=str, required=True,
                       choices=[
                           'focused', 'distracted',
                           'eyes_open', 'eyes_half_closed', 'eyes_closed',
                           'head_forward', 'head_tilted', 'head_sideways',
                           'hands_on_wheel', 'hands_off_wheel', 'holding_object'
                       ],
                       help='Class of data to collect')
    parser.add_argument('--samples', type=int, default=200,
                       help='Number of samples to collect')
    parser.add_argument('--delay', type=float, default=0.2,
                       help='Delay between captures in seconds')
    parser.add_argument('--no-detailed', dest='detailed', action='store_false',
                       help='Disable detailed data collection for subclasses')
    
    args = parser.parse_args()
    
    # Create directory structure
    create_directory_structure(args.dir)
    
    # Collect data
    collect_data(args.dir, args.class_name, args.samples, args.delay, args.detailed)

if __name__ == "__main__":
    main()