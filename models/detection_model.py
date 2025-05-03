import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
# Update imports for newer TensorFlow versions
try:
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
except ImportError:
    # For newer versions where keras is a separate package
    from keras.models import Sequential, load_model
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

class SafetyMonitoringModel:
    def __init__(self, eye_aspect_ratio_threshold=0.2, confidence_threshold=0.7, model_path=None):
        """
        Initialize the driver safety monitoring model
        
        Args:
            eye_aspect_ratio_threshold: Threshold for eye aspect ratio to determine drowsiness
            confidence_threshold: Confidence threshold for detection
            model_path: Path to a pre-trained model (if available)
        """
        self.eye_aspect_ratio_threshold = eye_aspect_ratio_threshold
        self.confidence_threshold = confidence_threshold
        
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
        # Left eye indices
        self.LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        # Right eye indices
        self.RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        # Head pose estimation points
        self.FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162]
        
        # Load or create model
        if model_path and os.path.exists(model_path):
            self.model = load_model(model_path)
        else:
            self.model = self._create_model()
            
    def _create_model(self):
        """Create a CNN model for distraction detection"""
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(2, activation='softmax')  # 2 classes: focused, distracted
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def save_model(self, path):
        """Save model to disk"""
        self.model.save(path)
        
    def _calculate_eye_aspect_ratio(self, eye_landmarks):
        """
        Calculate the eye aspect ratio (EAR) for detecting eye openness
        
        EAR = (h1 + h2) / (2 * w)
        where h1, h2 are the vertical distances between eye landmarks
        and w is the horizontal distance
        """
        # Vertical distances
        h1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        h2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        
        # Horizontal distance
        w = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        # Calculate EAR
        ear = (h1 + h2) / (2.0 * w) if w > 0 else 0
        
        return ear
    
    def _get_eye_landmarks(self, face_landmarks, image_shape):
        """Extract eye landmarks from face mesh result"""
        h, w = image_shape[:2]
        
        left_eye = np.array([
            [face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h]
            for i in self.LEFT_EYE_INDICES
        ], dtype=np.float32)
        
        right_eye = np.array([
            [face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h]
            for i in self.RIGHT_EYE_INDICES
        ], dtype=np.float32)
        
        return left_eye, right_eye
    
    def _estimate_head_pose(self, face_landmarks, image_shape):
        """Estimate head pose from face landmarks"""
        h, w = image_shape[:2]
        
        # Get face oval points
        face_oval = np.array([
            [face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h]
            for i in self.FACE_OVAL
        ], dtype=np.float32)
        
        # Fit an ellipse to the face oval
        if len(face_oval) > 5:  # Need at least 5 points to fit an ellipse
            ellipse = cv2.fitEllipse(face_oval.astype(np.int32))
            center, axes, angle = ellipse
            
            # Angle can be used to determine head tilt
            # angle = 0 means head is straight
            # Significant deviation indicates tilted head
            is_tilted = abs(angle - 90) > 15
            
            # Get face center coordinates
            nose_tip = face_landmarks.landmark[4]
            nose_x, nose_y = nose_tip.x * w, nose_tip.y * h
            
            # Determine if looking left/right
            # In general, if nose_x is significantly off-center, the person is looking to the side
            center_offset_x = abs(nose_x - (w / 2)) / (w / 2)
            is_looking_sideways = center_offset_x > 0.2
            
            return angle, is_tilted, is_looking_sideways
        
        return 0, False, False
    
    def _detect_hand_position(self, hands_result, image_shape):
        """Detect if hands are on the steering wheel or holding something else"""
        if not hands_result.multi_hand_landmarks:
            return "hands_not_visible"
        
        h, w = image_shape[:2]
        
        # For simplicity, we're just checking hand position in the image
        # In a real application, you would need a more sophisticated approach
        # to determine if hands are on steering wheel versus holding other objects
        
        hand_landmarks = hands_result.multi_hand_landmarks[0]
        
        # Get wrist position (landmark 0)
        wrist_x = hand_landmarks.landmark[0].x * w
        wrist_y = hand_landmarks.landmark[0].y * h
        
        # Define region boundaries for steering wheel (this is simplified)
        # Assuming the bottom center of the image is where the steering wheel would be
        steering_wheel_region_x = (w * 0.3, w * 0.7)  # 30-70% of width
        steering_wheel_region_y = (h * 0.6, h * 0.9)  # 60-90% of height
        
        if (steering_wheel_region_x[0] <= wrist_x <= steering_wheel_region_x[1] and 
            steering_wheel_region_y[0] <= wrist_y <= steering_wheel_region_y[1]):
            return "hands_on_wheel"
        else:
            return "hands_not_on_wheel"
    
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
            "confidence": 0.0
        }
        
        # Check if face was detected
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            
            # Get eye landmarks
            left_eye, right_eye = self._get_eye_landmarks(face_landmarks, frame.shape)
            
            # Calculate eye aspect ratio
            left_ear = self._calculate_eye_aspect_ratio(left_eye.reshape(-1, 2))
            right_ear = self._calculate_eye_aspect_ratio(right_eye.reshape(-1, 2))
            avg_ear = (left_ear + right_ear) / 2.0
            
            results["eye_aspect_ratio"] = avg_ear
            
            # Determine drowsiness based on eye aspect ratio
            results["drowsy"] = avg_ear < self.eye_aspect_ratio_threshold
            
            # Estimate head pose
            angle, is_tilted, is_looking_sideways = self._estimate_head_pose(face_landmarks, frame.shape)
            
            if is_looking_sideways:
                results["head_direction"] = "sideways"
            elif is_tilted:
                results["head_direction"] = "tilted"
            else:
                results["head_direction"] = "forward"
            
            # Extract face region for distraction classification
            # This is a simplified version; in practice, you would use a more sophisticated approach
            face_x, face_y = [], []
            for landmark in face_landmarks.landmark:
                face_x.append(landmark.x * w)
                face_y.append(landmark.y * h)
            
            # Get face bounding box
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
            
            # Resize for model input
            if face_img.size > 0:
                face_img = cv2.resize(face_img, (100, 100))
                face_img = face_img / 255.0  # Normalize
                
                # Predict with model
                prediction = self.model.predict(np.expand_dims(face_img, axis=0), verbose=0)
                distracted_prob = prediction[0][1]
                
                results["confidence"] = float(distracted_prob)
                results["distracted"] = distracted_prob > self.confidence_threshold
            
        # Check hand position
        if hand_results.multi_hand_landmarks:
            results["hand_position"] = self._detect_hand_position(hand_results, frame.shape)
            
            # If hands are not on wheel, mark as distracted
            if results["hand_position"] == "hands_not_on_wheel":
                results["distracted"] = True
        
        return results
    
    def train(self, train_data, train_labels, validation_data=None, validation_labels=None, epochs=10, batch_size=32):
        """
        Train the model on provided dataset
        
        Args:
            train_data: Training images
            train_labels: Training labels
            validation_data: Validation images
            validation_labels: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            History object with training metrics
        """
        if validation_data is not None and validation_labels is not None:
            history = self.model.fit(
                train_data, train_labels,
                validation_data=(validation_data, validation_labels),
                epochs=epochs,
                batch_size=batch_size
            )
        else:
            history = self.model.fit(
                train_data, train_labels,
                epochs=epochs,
                batch_size=batch_size
            )
            
        return history