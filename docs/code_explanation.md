# Drowsiness Detection System: Code Explanation

This document provides a detailed explanation of important functions, models, libraries, and mathematical formulas used in the drowsiness detection system.

## Core Detection Algorithms

### Eye Aspect Ratio (EAR) Calculation

The Eye Aspect Ratio (EAR) is a crucial metric used to determine the openness of the eyes. The mathematical formula for EAR is:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Where:
- p1 to p6 are facial landmarks corresponding to the eye
- ||p1-p4|| represents the Euclidean distance between points p1 and p4

In the code, this is implemented in `models/simple_model.py`:

```python
def _calculate_improved_ear(self, landmarks, left_eye_indices, right_eye_indices):
    """
    Calculate the Eye Aspect Ratio (EAR) for both eyes using facial landmarks.
    """
    # Extract coordinates for left and right eyes
    left_eye_points = np.array([landmarks[i] for i in left_eye_indices])
    right_eye_points = np.array([landmarks[i] for i in right_eye_indices])
    
    # Calculate EAR for left eye
    left_ear = self._calculate_single_ear(left_eye_points)
    
    # Calculate EAR for right eye
    right_ear = self._calculate_single_ear(right_eye_points)
    
    # Return the average EAR for both eyes
    return (left_ear + right_ear) / 2.0

def _calculate_single_ear(self, eye_points):
    """
    Calculate EAR for a single eye.
    Reference: Soukupová and Čech (2016) paper on real-time eye blink detection
    """
    # Calculate the vertical distances
    v1 = np.linalg.norm(eye_points[1] - eye_points[5])
    v2 = np.linalg.norm(eye_points[2] - eye_points[4])
    
    # Calculate the horizontal distance
    h = np.linalg.norm(eye_points[0] - eye_points[3])
    
    # Calculate EAR
    ear = (v1 + v2) / (2.0 * h)
    return ear
```

When the eyes are open, the EAR value is typically in the range of 0.25-0.35. When the eyes are closed, the EAR drops significantly, usually below 0.2. The system uses a configurable threshold (default at 0.2) to determine if the eyes are closed.

### Head Position Detection

Head position is determined by analyzing the orientation and position of facial landmarks relative to a reference position:

```python
def _detect_head_position(self, landmarks):
    """
    Detect head position using facial landmarks.
    Returns: straight, tilted, or turned_sideways
    """
    # Normalize landmarks to remove effects of distance from camera
    normalized_landmarks = self._normalize_landmarks(landmarks)
    
    # Extract key facial landmarks for orientation analysis
    nose_tip = normalized_landmarks[self.NOSE_TIP_INDEX]
    left_eye = normalized_landmarks[self.LEFT_EYE_CENTER_INDEX]
    right_eye = normalized_landmarks[self.RIGHT_EYE_CENTER_INDEX]
    
    # Calculate head rotation around Y-axis (turning left/right)
    eye_line_vector = right_eye - left_eye
    eye_line_center = (left_eye + right_eye) / 2
    nose_offset = nose_tip - eye_line_center
    
    # Calculate metrics
    horizontal_angle = np.arctan2(nose_offset[0], nose_offset[2])
    vertical_angle = np.arctan2(nose_offset[1], nose_offset[2])
    
    # Determine head position based on angles
    if abs(horizontal_angle) > self.HEAD_TURNED_THRESHOLD:
        return "turned_sideways"
    elif abs(vertical_angle) > self.HEAD_TILTED_THRESHOLD:
        return "tilted"
    else:
        return "straight"
```

### Hand Position Detection

The system monitors if the driver's hands are properly positioned on the steering wheel:

```python
def _detect_hand_position(self, hand_landmarks):
    """
    Detect if hands are on the steering wheel based on hand landmarks.
    Returns: on_wheel or not_on_wheel
    """
    if not hand_landmarks or len(hand_landmarks) < 1:
        return "not_on_wheel"
    
    # Define wheel area (this would be calibrated for each vehicle setup)
    wheel_center_x = 0.5  # center of frame
    wheel_center_y = 0.7  # lower part of frame
    wheel_radius = 0.2    # relative to frame size
    
    hands_on_wheel_count = 0
    
    # Check each detected hand
    for landmarks in hand_landmarks:
        # Use wrist position as the hand position indicator
        wrist_landmark = landmarks[0]
        
        # Calculate distance from wheel center
        distance = np.sqrt((wrist_landmark[0] - wheel_center_x)**2 + 
                          (wrist_landmark[1] - wheel_center_y)**2)
        
        # Check if hand is on wheel
        if distance <= wheel_radius:
            hands_on_wheel_count += 1
    
    # At least one hand should be on the wheel
    if hands_on_wheel_count >= 1:
        return "on_wheel"
    else:
        return "not_on_wheel"
```

## Machine Learning Models

### SVM Classifier (simple_model.py)

The system uses a Support Vector Machine (SVM) for classification of driver states:

```python
def _extract_simple_features(self, face_landmarks, hands_landmarks, ear_value, 
                            head_position, hand_position, frame_shape):
    """
    Extract features for SVM classification
    """
    features = []
    
    # EAR feature
    features.append(ear_value)
    
    # Head position features - one-hot encoding
    head_pos_features = [0, 0, 0]  # [straight, tilted, turned_sideways]
    if head_position == "straight":
        head_pos_features[0] = 1
    elif head_position == "tilted":
        head_pos_features[1] = 1
    elif head_position == "turned_sideways":
        head_pos_features[2] = 1
    features.extend(head_pos_features)
    
    # Hand position feature - binary
    hand_pos_feature = 1 if hand_position == "on_wheel" else 0
    features.append(hand_pos_feature)
    
    # Additional geometric features from landmarks
    if face_landmarks is not None:
        # Calculate angles between specific landmarks
        # Add normalized distances between key points
        pass
    
    return np.array(features)
```

The SVM model is trained using labeled data collected from the data collection module:

```python
def train(self, X_train, y_train):
    """
    Train the SVM model
    """
    # Normalize features
    self.scaler = StandardScaler()
    X_train_normalized = self.scaler.fit_transform(X_train)
    
    # Train SVM model
    self.model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
    self.model.fit(X_train_normalized, y_train)
    
    return self.model
```

### CNN Model (detection_model.py)

For more advanced detection, a Convolutional Neural Network (CNN) is implemented:

```python
def _create_model(self):
    """
    Create a CNN architecture for drowsiness detection
    """
    model = Sequential([
        # First convolution block
        Conv2D(32, (3, 3), padding='same', input_shape=(self.img_height, self.img_width, 6)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Second convolution block
        Conv2D(64, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Third convolution block
        Conv2D(128, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Dropout layer to prevent overfitting
        Dropout(0.5),
        
        # Flatten and Dense layers
        Flatten(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(2, activation='softmax')  # 2 classes: focused/distracted
    ])
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model
```

## Libraries and Dependencies

### Computer Vision and Machine Learning

1. **OpenCV** (cv2):
   - Used for image processing operations
   - Camera handling and frame capture
   - Basic face detection using Haar cascades or DNN models
   - Drawing annotations on frames

2. **MediaPipe**:
   - Face mesh for detecting 468 facial landmarks
   - Hand tracking for detecting 21 points on each hand
   - Provides 3D coordinates for more accurate spatial analysis

3. **scikit-learn**:
   - SVM implementation for classification
   - Feature standardization with StandardScaler
   - Metrics for model evaluation (accuracy, precision, recall)

4. **NumPy**:
   - Efficient array operations for landmark manipulation
   - Mathematical computations for EAR and other metrics
   - Feature vector handling

### User Interface and Audio

1. **PyQt5**:
   - Main application window
   - Real-time video display
   - Configuration controls
   - Status indicators and metrics display

2. **PyAudio**:
   - Audio playback for alert sounds
   - Audio capture for voice commands (future enhancement)

## Detection Pipeline

The complete detection pipeline can be summarized as:

1. **Frame Acquisition**:
   - Capture frame from camera using OpenCV

2. **Face Detection**:
   - Detect face in frame using MediaPipe Face Detection

3. **Landmark Detection**:
   - Extract 468 facial landmarks using MediaPipe Face Mesh
   - Extract hand landmarks if hands are visible

4. **Feature Extraction**:
   - Calculate EAR from eye landmarks
   - Determine head position from facial landmarks
   - Detect hand position relative to steering wheel area

5. **State Classification**:
   - Extract feature vector
   - Normalize features
   - Apply SVM or CNN model for classification

6. **Temporal Smoothing**:
   - Apply sliding window to reduce false positives
   - Require consecutive detections for alert triggering

7. **Alert System**:
   - Visual alerts on UI
   - Audio alerts for detected states
   - Record violations for later analysis

## State Machine Logic

The system implements a simple state machine to manage driver states:

```
NORMAL_STATE ⟷ WARNING_STATE ⟷ ALERT_STATE
```

Transitions between states are managed based on detection confidence and duration:

```python
def update_driver_state(self, drowsy, distracted):
    """
    Update the driver state based on detection results
    """
    # State transition logic
    if drowsy or distracted:
        self.consecutive_detections += 1
        
        if self.state == "NORMAL" and self.consecutive_detections >= self.WARNING_THRESHOLD:
            self.state = "WARNING"
            
        elif self.state == "WARNING" and self.consecutive_detections >= self.ALERT_THRESHOLD:
            self.state = "ALERT"
            return True  # Trigger alert
    else:
        self.consecutive_detections = 0
        
        if self.state != "NORMAL":
            self.recovery_frames += 1
            if self.recovery_frames >= self.RECOVERY_THRESHOLD:
                self.state = "NORMAL"
                self.recovery_frames = 0
                
    return False  # No alert needed
```

## Testing Methodology

Testing strategies implemented in the system:

### Unit Testing

Individual components are tested in isolation:

```python
def test_eye_aspect_ratio():
    model = SimpleSafetyModel()
    
    # Test with open eyes landmarks
    open_eye_landmarks = load_test_landmarks("open_eyes.json")
    open_ear = model._calculate_improved_ear(
        open_eye_landmarks, 
        model.LEFT_EYE_INDICES, 
        model.RIGHT_EYE_INDICES
    )
    
    # Test with closed eyes landmarks
    closed_eye_landmarks = load_test_landmarks("closed_eyes.json")
    closed_ear = model._calculate_improved_ear(
        closed_eye_landmarks, 
        model.LEFT_EYE_INDICES, 
        model.RIGHT_EYE_INDICES
    )
    
    # Verify results
    assert open_ear > 0.25, f"Open eye EAR should be >0.25, got {open_ear}"
    assert closed_ear < 0.2, f"Closed eye EAR should be <0.2, got {closed_ear}"
    assert open_ear > closed_ear, "Open eye EAR should be greater than closed eye EAR"
```

### Integration Testing

Testing how components work together:

```python
def test_full_detection_pipeline():
    # Initialize model
    model = SimpleSafetyModel()
    
    # Test with different sample images
    for test_case in ["normal.jpg", "drowsy.jpg", "distracted.jpg"]:
        # Load test image
        frame = cv2.imread(f"test_data/{test_case}")
        
        # Process frame
        results = model.process_frame(frame)
        
        # Check results based on test case
        if "normal" in test_case:
            assert not results["drowsy"] and not results["distracted"]
        elif "drowsy" in test_case:
            assert results["drowsy"] and not results["distracted"]
        elif "distracted" in test_case:
            assert not results["drowsy"] and results["distracted"]
```

### Performance Testing

Ensuring the system can operate in real-time:

```python
def test_processing_speed():
    model = SimpleSafetyModel()
    
    # Load test frame
    frame = cv2.imread("test_data/benchmark.jpg")
    
    # Warmup
    model.process_frame(frame)
    
    # Benchmark
    iterations = 100
    start_time = time.time()
    
    for _ in range(iterations):
        model.process_frame(frame)
        
    total_time = time.time() - start_time
    avg_time = total_time / iterations
    
    # Assert processing is fast enough for real-time operation
    assert avg_time < 0.05, f"Average processing time too slow: {avg_time:.4f}s"
```

## Future Enhancement Directions

Potential improvements for the system:

1. **Deep Learning Enhancements**:
   - Replace SVM with more sophisticated deep learning models
   - Implement attention mechanisms for better feature extraction
   - Use temporal models (LSTM/GRU) for better time-series analysis

2. **Additional Detection Features**:
   - Gaze tracking to detect driver attention focus
   - Yawning detection as an additional drowsiness indicator
   - Phone usage detection for distraction monitoring

3. **System Improvements**:
   - Edge processing optimization for embedded deployment
   - Multi-camera setup for better coverage of driver
   - Integration with vehicle telematics data

4. **User Experience**:
   - Personalized alert thresholds based on driver history
   - Voice-based alerts and interaction
   - Dashboard integration for commercial vehicles
