import cv2
import numpy as np
import mediapipe as mp
import os
import pickle
import time

class SimpleSafetyModel:
    def __init__(self, eye_aspect_ratio_threshold=0.2, confidence_threshold=0.7, model_path=None):
        """
        Initialize the driver safety monitoring model using scikit-learn instead of TensorFlow
        
        Args:
            eye_aspect_ratio_threshold: Threshold for eye aspect ratio to determine drowsiness
            confidence_threshold: Confidence threshold for detection
            model_path: Path to a pre-trained model (if available)
        """
        self.eye_aspect_ratio_threshold = eye_aspect_ratio_threshold
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.scaler = None
        
        # Initialize MediaPipe face mesh for facial landmarks
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize MediaPipe hands for hand tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Face landmark indices for eyes
        # Left eye indices (improved with more precise landmarks)
        self.LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        # Define the critical points for EAR calculation (vertical and horizontal)
        self.LEFT_EYE_VERTICAL_1 = [386, 374]
        self.LEFT_EYE_VERTICAL_2 = [385, 380]
        self.LEFT_EYE_VERTICAL_3 = [387, 373]
        self.LEFT_EYE_HORIZONTAL = [362, 263]
        
        # Right eye indices (improved with more precise landmarks)
        self.RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        # Define the critical points for EAR calculation (vertical and horizontal)
        self.RIGHT_EYE_VERTICAL_1 = [159, 145]
        self.RIGHT_EYE_VERTICAL_2 = [158, 153]
        self.RIGHT_EYE_VERTICAL_3 = [160, 144]
        self.RIGHT_EYE_HORIZONTAL = [33, 133]
        
        # Head pose estimation points
        self.FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162]
        
        # Initialize DNN-based face detector for better accuracy
        self.use_dnn_face_detector = True
        try:
            # Pre-trained model files
            model_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "models", "opencv_face_detector_uint8.pb")
            config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      "models", "opencv_face_detector.pbtxt")
            
            # Check if files exist first
            if os.path.exists(model_file) and os.path.exists(config_file):
                self.face_net = cv2.dnn.readNet(model_file, config_file)
                print("DNN face detector loaded successfully")
            else:
                self.use_dnn_face_detector = False
                print("DNN face detector model files not found, falling back to MediaPipe")
        except Exception as e:
            self.use_dnn_face_detector = False
            print(f"Failed to load DNN face detector: {e}, falling back to MediaPipe")
            
        # Blink detection variables
        self.blink_counter = 0
        self.blink_total = 0
        self.blink_start_time = time.time()
        self.EYE_AR_CONSEC_FRAMES = 3  # Number of consecutive frames the eye must be below threshold to count as a blink
        self.last_ear_values = []
        self.MAX_EAR_HISTORY = 10
        
        # Consecutive frames tracking for drowsiness
        self.DROWSY_CONSEC_FRAMES = 20  # Need 20 consecutive frames to confirm drowsiness
        self.drowsy_frame_counter = 0
        self.is_drowsy = False
        
        # Consecutive frames tracking for distraction
        self.DISTRACTED_CONSEC_FRAMES = 25  # Updated: Need 25 consecutive frames to confirm head-only distraction
        self.DISTRACTED_HEAD_HANDS_CONSEC_FRAMES = 20  # New: Need 20 consecutive frames to confirm combined head+hands distraction
        self.HEAD_OUT_OF_FRAME_CONSEC_FRAMES = 10  # Need 10 consecutive frames to confirm head is out of frame
        self.distracted_frame_counter = 0
        self.distracted_head_hands_counter = 0
        self.head_out_of_frame_counter = 0
        self.is_distracted = False
        self.is_head_hands_distracted = False
        self.head_out_of_frame = False
        
        # Historic state information
        self.ear_history = []
        self.head_pose_history = []
        self.hand_position_history = []
        
        # Load model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load the model from disk"""
        try:
            with open(model_path, 'rb') as f:
                self.model, self.scaler = pickle.load(f)
            print(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def _calculate_eye_aspect_ratio(self, landmarks, image_shape):
        """
        Calculate the eye aspect ratio (EAR) for detecting eye openness
        This improved version uses specific landmarks for more accurate EAR calculation
        
        EAR = (|v1| + |v2| + |v3|) / (2 * |h|)
        where v1, v2, v3 are the vertical distances between eye landmarks
        and h is the horizontal distance
        """
        h, w = image_shape[:2]
        
        # Helper function to get point coordinates from landmark index
        def get_point(idx):
            return np.array([landmarks.landmark[idx].x * w, landmarks.landmark[idx].y * h])
        
        # Left eye
        # Get vertical distances (3 pairs)
        l_v1 = np.linalg.norm(get_point(self.LEFT_EYE_VERTICAL_1[0]) - get_point(self.LEFT_EYE_VERTICAL_1[1]))
        l_v2 = np.linalg.norm(get_point(self.LEFT_EYE_VERTICAL_2[0]) - get_point(self.LEFT_EYE_VERTICAL_2[1]))
        l_v3 = np.linalg.norm(get_point(self.LEFT_EYE_VERTICAL_3[0]) - get_point(self.LEFT_EYE_VERTICAL_3[1]))
        
        # Get horizontal distance
        l_h = np.linalg.norm(get_point(self.LEFT_EYE_HORIZONTAL[0]) - get_point(self.LEFT_EYE_HORIZONTAL[1]))
        
        # Calculate left EAR
        left_ear = (l_v1 + l_v2 + l_v3) / (3.0 * l_h) if l_h > 0 else 0
        
        # Right eye
        # Get vertical distances (3 pairs)
        r_v1 = np.linalg.norm(get_point(self.RIGHT_EYE_VERTICAL_1[0]) - get_point(self.RIGHT_EYE_VERTICAL_1[1]))
        r_v2 = np.linalg.norm(get_point(self.RIGHT_EYE_VERTICAL_2[0]) - get_point(self.RIGHT_EYE_VERTICAL_2[1]))
        r_v3 = np.linalg.norm(get_point(self.RIGHT_EYE_VERTICAL_3[0]) - get_point(self.RIGHT_EYE_VERTICAL_3[1]))
        
        # Get horizontal distance
        r_h = np.linalg.norm(get_point(self.RIGHT_EYE_HORIZONTAL[0]) - get_point(self.RIGHT_EYE_HORIZONTAL[1]))
        
        # Calculate right EAR
        right_ear = (r_v1 + r_v2 + r_v3) / (3.0 * r_h) if r_h > 0 else 0
        
        # Average EAR from both eyes
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Add to ear history for blink detection
        self.last_ear_values.append(avg_ear)
        if len(self.last_ear_values) > self.MAX_EAR_HISTORY:
            self.last_ear_values.pop(0)
        
        return left_ear, right_ear, avg_ear
    
    def _detect_blinks(self, ear):
        """
        Detect eye blinks based on EAR values
        A high frequency of blinks can indicate drowsiness
        """
        # Check if EAR is below threshold
        if ear < self.eye_aspect_ratio_threshold:
            self.blink_counter += 1
        else:
            # Check if a blink was detected
            if self.blink_counter >= self.EYE_AR_CONSEC_FRAMES:
                self.blink_total += 1
            self.blink_counter = 0
        
        # Calculate blink rate (blinks per minute)
        elapsed_time = time.time() - self.blink_start_time
        blink_rate = 0
        
        if elapsed_time > 0:
            blink_rate = (self.blink_total / elapsed_time) * 60
            
            # Reset counters every minute
            if elapsed_time >= 60:
                self.blink_start_time = time.time()
                self.blink_total = 0
        
        return blink_rate
    
    def _detect_faces_dnn(self, frame):
        """
        Detect faces using DNN-based face detector for higher accuracy
        
        Returns:
            List of bounding boxes in format (x, y, w, h)
        """
        h, w = frame.shape[:2]
        faces = []
        
        # Create a blob from the image
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        
        # Set the blob as input to the network
        self.face_net.setInput(blob)
        
        # Forward pass through the network
        detections = self.face_net.forward()
        
        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            # Filter detections based on confidence
            if confidence > 0.5:
                # Get bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                
                # Ensure coordinates are within frame bounds
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                faces.append((x1, y1, x2 - x1, y2 - y1))
        
        return faces
    
    def _estimate_head_pose(self, face_landmarks, image_shape):
        """
        Estimate head pose using facial landmarks
        
        Args:
            face_landmarks: MediaPipe face landmarks
            image_shape: Shape of the image
            
        Returns:
            tuple: (head angle in degrees, is_tilted flag, is_looking_sideways flag)
        """
        h, w = image_shape[:2]
        
        # Helper function to get point coordinates from landmark index
        def get_point(idx):
            return np.array([face_landmarks.landmark[idx].x * w, face_landmarks.landmark[idx].y * h])
        
        # Get key facial points to determine head pose
        # Use face oval points for better orientation estimation
        face_points = []
        for idx in self.FACE_OVAL:
            x = face_landmarks.landmark[idx].x * w
            y = face_landmarks.landmark[idx].y * h
            face_points.append((x, y))
        
        face_points = np.array(face_points, dtype=np.float32)
        
        # Get facial center points
        left_eye_center = np.mean([get_point(idx) for idx in self.LEFT_EYE_INDICES], axis=0)
        right_eye_center = np.mean([get_point(idx) for idx in self.RIGHT_EYE_INDICES], axis=0)
        
        # Calculate horizontal eye line
        eye_line = right_eye_center - left_eye_center
        
        # Calculate angle of eye line with horizontal
        angle_rad = np.arctan2(eye_line[1], eye_line[0])  # in radians
        angle_deg = np.degrees(angle_rad)
        
        # Normalize angle to be between -90 and 90
        if angle_deg > 90:
            angle_deg = angle_deg - 180
        elif angle_deg < -90:
            angle_deg = angle_deg + 180
        
        # Calculate yaw based on face aspect ratio (width/height)
        face_width = max(face_points[:, 0]) - min(face_points[:, 0])
        face_height = max(face_points[:, 1]) - min(face_points[:, 1])
        
        # Aspect ratio depends on head rotation
        face_aspect_ratio = face_width / face_height if face_height > 0 else 0
        
        # Get nose tip and eye center distances for yaw estimation
        nose_tip = get_point(4)  # Nose tip landmark index
        face_center = (left_eye_center + right_eye_center) / 2
        midpoint_x = (left_eye_center[0] + right_eye_center[0]) / 2
        
        # Calculate nose deviation from midpoint (indicates sideways looking)
        nose_deviation = (nose_tip[0] - midpoint_x) / face_width if face_width > 0 else 0
        
        # Determine head orientation states - increased thresholds to reduce false positives
        is_tilted = abs(angle_deg) > 20  # Increased from 15 to 20 degrees for tilt detection
        is_looking_sideways = abs(nose_deviation) > 0.15  # Increased from 0.1 to 0.15 for sideways detection
        
        return angle_deg, is_tilted, is_looking_sideways
    
    def _extract_features(self, face_img, img_size=(100, 100)):
        """
        Extract features from face image for model prediction
        
        Args:
            face_img: Face image region
            img_size: Size to resize the image to
            
        Returns:
            Features array for model prediction
        """
        if face_img.size == 0 or face_img is None:
            return np.zeros((1, 121))  # Return zeros with correct feature dimension
            
        # Resize image
        try:
            img = cv2.resize(face_img, img_size)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return np.zeros((1, 121))
            
        # Convert to grayscale for feature extraction
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
        
        # Calculate features
        features = []
        
        # Add average pixel values in different regions as features
        cell_size = 20
        for i in range(0, img_size[0], cell_size):
            for j in range(0, img_size[1], cell_size):
                cell = gray[i:i+cell_size, j:j+cell_size]
                if cell.size > 0:
                    features.append(np.mean(cell))
        
        # Add histogram features - more bins for better representation
        img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        for channel in range(3):
            hist = cv2.calcHist([img_rgb], [channel], None, [32], [0, 256])
            features.extend(hist.flatten())
            
        # Add Gabor filter features for better texture representation
        ksize = 9
        for theta in [0, np.pi/4, np.pi/2, 3*np.pi/4]:
            gabor_kernel = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, cv2.CV_32F)
            filtered_img = cv2.filter2D(gray, cv2.CV_8UC3, gabor_kernel)
            # Sample points from filtered image
            step = 20
            for i in range(0, filtered_img.shape[0], step):
                for j in range(0, filtered_img.shape[1], step):
                    if i < filtered_img.shape[0] and j < filtered_img.shape[1]:
                        features.append(filtered_img[i, j])
        
        # Make sure we have exactly 121 features
        if len(features) < 121:
            features.extend([0] * (121 - len(features)))
        elif len(features) > 121:
            features = features[:121]
            
        return np.array([features])
    
    def process_frame(self, frame):
        """
        Process a video frame to detect drowsiness and distraction
        
        Returns:
            dict: Detection results containing drowsiness state, distraction indicators, and confidence
        """
        if frame is None:
            return {
                "error": "Invalid frame",
                "drowsy": False,
                "distracted": False
            }
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        
        # Detect faces using DNN if available
        face_detected_by_dnn = False
        face_box = None
        
        if self.use_dnn_face_detector:
            try:
                faces = self._detect_faces_dnn(frame)
                if faces:
                    face_detected_by_dnn = True
                    # Use the largest face (closest to camera)
                    face_box = max(faces, key=lambda box: box[2] * box[3])
            except Exception as e:
                print(f"DNN face detection failed: {e}")
        
        # Process with face mesh
        face_results = self.face_mesh.process(rgb_frame)
        
        # Process with hand detection
        hand_results = self.hands.process(rgb_frame)
        
        results = {
            "drowsy": False,
            "distracted": False,
            "eye_aspect_ratio": 0,
            "head_direction": "forward",
            "hand_position": "unknown",
            "confidence": 0.0,
            "blink_rate": 0
        }
        
        # Check if face is out of frame (not detected by MediaPipe or DNN)
        if not face_results.multi_face_landmarks and not face_detected_by_dnn:
            self.head_out_of_frame_counter += 1
        else:
            self.head_out_of_frame_counter = 0
            
        # If head has been out of frame for enough consecutive frames, mark as distracted
        if self.head_out_of_frame_counter >= self.HEAD_OUT_OF_FRAME_CONSEC_FRAMES:
            results["distracted"] = True
            results["head_direction"] = "out_of_frame"
            results["distraction_type"] = "head_out_of_frame"
            self.head_out_of_frame = True
            self.is_distracted = True  # Set the distracted state to true
            return results  # Return early since we can't process further without a face
        else:
            self.head_out_of_frame = False
        
        # First detect hand position - this is now prioritized for phone detection
        hand_position = "unknown"
        is_holding_phone = False
        
        if hand_results.multi_hand_landmarks:
            hand_position = self._detect_hand_position(hand_results.multi_hand_landmarks, frame.shape)
            # Check if phone is directly detected
            if hand_position == "phone_detected":
                is_holding_phone = True
                # Immediately mark as distracted for phone usage - no need for consecutive frames
                results["distracted"] = True
                results["distraction_type"] = "phone_usage"
                self.is_head_hands_distracted = True
                self.distracted_head_hands_counter = self.DISTRACTED_HEAD_HANDS_CONSEC_FRAMES
            # Otherwise check other hand positions
            elif hand_position == "hands_not_on_wheel":
                # Analyze hand position for phone patterns
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    # Check for phone holding pattern: Look at middle finger and thumb positions
                    thumb_tip = hand_landmarks.landmark[4]  # MediaPipe thumb tip
                    middle_tip = hand_landmarks.landmark[12]  # MediaPipe middle finger tip
                    
                    # If thumb and middle finger are at similar height, likely holding phone
                    if abs(thumb_tip.y - middle_tip.y) < 0.05:
                        is_holding_phone = True
                        break
            results["hand_position"] = hand_position
            results["is_holding_phone"] = is_holding_phone
        else:
            # If hands were not detected, assume they might be on the wheel but not visible
            hand_position = "hands_on_wheel"
            results["hand_position"] = hand_position
            results["is_holding_phone"] = False
            
        # Check if face was detected by MediaPipe
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            
            # Calculate enhanced eye aspect ratio with the improved method
            left_ear, right_ear, avg_ear = self._calculate_eye_aspect_ratio(face_landmarks, frame.shape)
            results["eye_aspect_ratio"] = avg_ear
            
            # Detect blinks
            blink_rate = self._detect_blinks(avg_ear)
            results["blink_rate"] = blink_rate
            
            # Determine drowsiness based on eye aspect ratio and blink rate
            # Track consecutive frames for drowsiness detection
            if avg_ear < self.eye_aspect_ratio_threshold or blink_rate > 25:
                self.drowsy_frame_counter += 1
            else:
                self.drowsy_frame_counter = 0
                
            # Only mark as drowsy if we have enough consecutive frames
            if self.drowsy_frame_counter >= self.DROWSY_CONSEC_FRAMES:
                results["drowsy"] = True
                self.is_drowsy = True
            else:
                results["drowsy"] = False
                self.is_drowsy = False
            
            # Estimate head pose
            angle, is_tilted, is_looking_sideways = self._estimate_head_pose(face_landmarks, frame.shape)
            
            # Record the head direction for reporting
            if is_looking_sideways:
                results["head_direction"] = "sideways"
            elif is_tilted:
                results["head_direction"] = "tilted"
            else:
                results["head_direction"] = "forward"
            
            # Enhanced distraction detection with improved phone usage detection
            is_head_distracted = self._detect_head_distraction(angle, is_tilted, is_looking_sideways)
            
            # Skip phone usage check if we've already determined phone use directly
            if not results["distracted"]:
                # Phone usage is now a primary indicator of distraction
                if is_holding_phone:
                    # Immediately count as distracted if phone is detected, with a very short detection window
                    self.distracted_head_hands_counter += 5  # Much faster accumulation for confirmed phone usage
                    
                    # If EAR is in the typical phone viewing range, immediately mark as distracted
                    if 0.22 <= avg_ear <= 0.28:
                        self.distracted_head_hands_counter = self.DISTRACTED_HEAD_HANDS_CONSEC_FRAMES
                elif hand_position == "hands_not_on_wheel":
                    # Increment counter more slowly for just hands off wheel
                    self.distracted_head_hands_counter += 2
                else:
                    # Decrease counter more slowly to prevent false negatives during momentary detection gaps
                    self.distracted_head_hands_counter = max(0, self.distracted_head_hands_counter - 1)
                
                # Track consecutive frames for head-only distraction
                if is_head_distracted:
                    self.distracted_frame_counter += 1
                else:
                    self.distracted_frame_counter = 0
                
                # Check if either distraction condition is met
                if self.distracted_frame_counter >= self.DISTRACTED_CONSEC_FRAMES:
                    results["distracted"] = True
                    results["distraction_type"] = "head_position"
                    self.is_distracted = True
                elif self.distracted_head_hands_counter >= self.DISTRACTED_HEAD_HANDS_CONSEC_FRAMES:
                    results["distracted"] = True
                    results["distraction_type"] = "phone_usage"
                    self.is_head_hands_distracted = True
                else:
                    results["distracted"] = False
                    self.is_distracted = False
                    self.is_head_hands_distracted = False
            
            # Extract face region for distraction classification
            face_x, face_y = [], []
            for landmark in face_landmarks.landmark:
                face_x.append(landmark.x * w)
                face_y.append(landmark.y * h)
            
            # Use DNN detection if available, otherwise use MediaPipe landmarks
            if face_detected_by_dnn:
                x, y, width, height = face_box
                # Add padding
                padding = int(min(width, height) * 0.1)
                x_min = max(0, x - padding)
                y_min = max(0, y - padding)
                x_max = min(w, x + width + padding)
                y_max = min(h, y + height + padding)
            else:
                # Get face bounding box from landmarks
                x_min, x_max = int(min(face_x)), int(max(face_x))
                y_min, y_max = int(min(face_y)), int(max(face_y))
                
                # Add padding
                padding = 20
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)
            
            # Extract face region
            face_img = frame[y_min:y_max, x_min:x_max]
            
            # Make prediction if model is loaded and face is detected
            if self.model is not None and face_img.size > 0:
                # Extract features
                features = self._extract_features(face_img)
                
                # Scale features
                if self.scaler is not None:
                    features = self.scaler.transform(features)
                
                # Predict - but only use as additional information, not as the primary decision factor
                if hasattr(self.model, 'predict_proba'):
                    # Get probability of distraction
                    proba = self.model.predict_proba(features)[0]
                    distracted_prob = proba[1]  # Probability of class 1 (distracted)
                    results["confidence"] = float(distracted_prob)
                else:
                    # Simple prediction (no probability)
                    prediction = self.model.predict(features)[0]
                    results["confidence"] = 1.0 if prediction == 1 else 0.0
        
        return results
    
    def _detect_hand_position(self, hand_landmarks, frame_shape):
        """
        Detect hand position based on MediaPipe hand landmarks
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            frame_shape: Shape of the frame
            
        Returns:
            str: Hand position - "hands_on_wheel", "hands_off_wheel", or "phone_detected"
        """
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return "unknown"
        
        # Frame dimensions
        frame_height, frame_width = frame_shape[:2]
        
        # Define regions
        wheel_region_y = int(frame_height * 0.6)  # Lower 40% of the frame
        
        # Phone holding detection patterns
        phone_detected = False
        
        for hand in hand_landmarks:
            # Check if hand is in a phone-holding position
            palm_points = [0, 1, 5, 9, 13, 17]  # Palm landmarks
            finger_points = [8, 12, 16, 20]  # Fingertips
            
            # Get palm and fingertip coordinates
            palm_coords = np.array([[hand.landmark[i].x * frame_width, 
                                   hand.landmark[i].y * frame_height] 
                                   for i in palm_points])
            
            finger_coords = np.array([[hand.landmark[i].x * frame_width, 
                                     hand.landmark[i].y * frame_height] 
                                     for i in finger_points])
            
            # Calculate if fingers are clustered together (phone holding pattern)
            finger_spread = np.std(finger_coords, axis=0)
            tight_grip = np.mean(finger_spread) < (frame_width * 0.1)
            
            # Calculate if palm is vertical (typical phone holding position)
            palm_vertical = False
            if len(palm_coords) >= 4:
                # Check if palm landmarks form a more vertical than horizontal shape
                palm_width = np.max(palm_coords[:, 0]) - np.min(palm_coords[:, 0])
                palm_height = np.max(palm_coords[:, 1]) - np.min(palm_coords[:, 1])
                palm_vertical = palm_height > palm_width
            
            # Check for specific thumb-index pinch pattern (selfie or phone holding)
            thumb_tip = np.array([hand.landmark[4].x * frame_width, hand.landmark[4].y * frame_height])
            index_tip = np.array([hand.landmark[8].x * frame_width, hand.landmark[8].y * frame_height])
            pinch_distance = np.linalg.norm(thumb_tip - index_tip)
            pinch_detected = pinch_distance < (frame_width * 0.05)
            
            # Check if hand is at face height (typical for phone use)
            hand_center_y = np.mean(palm_coords[:, 1])
            at_face_level = hand_center_y < wheel_region_y
            
            # Detect phone use based on combined criteria
            if ((tight_grip and palm_vertical) or pinch_detected) and at_face_level:
                phone_detected = True
                break
        
        # If phone detected, return this as highest priority
        if phone_detected:
            return "phone_detected"
        
        # Otherwise check if hands are on the wheel
        hands_on_wheel = False
        for hand in hand_landmarks:
            # Check if any hand is in the lower region (wheel region)
            hand_points = np.array([[hand.landmark[i].x * frame_width, 
                                   hand.landmark[i].y * frame_height] 
                                   for i in range(len(hand.landmark))])
            
            # If majority of hand points are in wheel region, consider hand on wheel
            points_in_wheel_region = np.sum(hand_points[:, 1] > wheel_region_y)
            if points_in_wheel_region > len(hand_points) / 2:
                hands_on_wheel = True
                break
        
        return "hands_on_wheel" if hands_on_wheel else "hands_off_wheel"
    
    def _detect_head_distraction(self, angle, is_tilted, is_looking_sideways):
        """
        Determine if the head position indicates distraction
        
        Args:
            angle: Head tilt angle in degrees
            is_tilted: Boolean indicating if head is tilted beyond threshold
            is_looking_sideways: Boolean indicating if head is turned sideways
            
        Returns:
            Boolean: True if head position indicates distraction
        """
        # Head is considered distracted if either significantly tilted or looking sideways
        return is_tilted or is_looking_sideways