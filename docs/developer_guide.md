# Drowsiness Detection System: Developer Guide

This guide provides technical information for developers who want to extend, modify, or integrate with the Drowsiness Detection System.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Code Structure](#code-structure)
- [Core Classes and Methods](#core-classes-and-methods)
- [Adding New Features](#adding-new-features)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Integration Points](#integration-points)
- [Best Practices](#best-practices)

## Architecture Overview

The system follows a modular architecture with clear separation of concerns:

![Architecture Diagram](assets/images/architecture.png)

### Core Components

1. **Detection Engine**
   - Face and landmark detection
   - Feature extraction
   - State classification

2. **User Interface**
   - Camera feed display
   - Status indicators
   - Configuration controls

3. **Data Management**
   - Data collection
   - Model training
   - Configuration storage

4. **Alert System**
   - Visual alerts
   - Audio notification
   - Alert logging

### Data Flow

```
Input Camera → Frame Acquisition → Face Detection → Landmark Detection → 
Feature Extraction → State Classification → Alert Generation → User Interface
```

## Code Structure

The codebase is organized into logical modules:

### Main Modules

| Module | Path | Description |
|--------|------|-------------|
| Main Entry | `main.py` | Application entry point with argument parsing |
| Detection Models | `models/` | Detection algorithms and models |
| User Interface | `ui/` | PyQt5-based user interface components |
| Data Collection | `data/` | Tools for gathering training data |
| Training | `training/` | Scripts for model training |
| Utilities | `utils/` | Helper functions and shared utilities |

### Key Files and Their Roles

- `main.py`: Entry point, command-line parsing, mode selection
- `models/simple_model.py`: Lightweight SVM-based detection model
- `models/detection_model.py`: More advanced CNN-based detection model
- `ui/monitoring_app.py`: Main monitoring interface implementation
- `training/simple_train.py`: SVM model training implementation
- `training/train_model.py`: CNN model training implementation
- `data/collect_data.py`: Data collection tool
- `utils/helpers.py`: Shared utility functions

## Core Classes and Methods

### SimpleSafetyModel (`models/simple_model.py`)

The core detection model using SVM classification:

```python
class SimpleSafetyModel:
    """
    Lightweight model for drowsiness and distraction detection using SVM.
    
    Main methods:
    - process_frame(frame): Process a video frame and return detection results
    - _calculate_improved_ear(landmarks, left_eye_indices, right_eye_indices): Calculate EAR
    - _detect_head_position(landmarks): Detect head orientation
    - _detect_hand_position(hand_landmarks): Check if hands are on the wheel
    - _extract_simple_features(...): Extract features for classification
    - load_model(model_path): Load a pre-trained model
    """
```

#### Key Methods

```python
def process_frame(self, frame):
    """
    Process a video frame and detect drowsiness/distraction.
    
    Args:
        frame: BGR image from camera
        
    Returns:
        dict: Detection results including:
            - drowsy (bool): Whether driver appears drowsy
            - distracted (bool): Whether driver appears distracted
            - ear (float): Current Eye Aspect Ratio value
            - ear_threshold (float): Current EAR threshold
            - head_position (str): Detected head position
            - hand_position (str): Detected hand position
            - confidence (float): Detection confidence
            - face_detected (bool): Whether a face was detected
    """
```

### DriverMonitoringUI (`ui/monitoring_app.py`)

The main user interface class:

```python
class DriverMonitoringUI(QMainWindow):
    """
    Main monitoring interface using PyQt5.
    
    Main methods:
    - start_camera(): Start camera feed
    - stop_camera(): Stop camera feed
    - update_frame(): Process and display camera frame
    - check_and_trigger_alerts(): Check detection results and issue alerts
    - save_settings(): Save user configuration to file
    - load_settings(): Load user configuration from file
    """
```

### SimpleModelTrainer (`training/simple_train.py`)

The model training class:

```python
class SimpleModelTrainer:
    """
    Trains SVM model for drowsiness and distraction detection.
    
    Main methods:
    - load_and_preprocess_data(): Load training images and preprocess
    - extract_features(): Extract features from images
    - train(): Train SVM on extracted features
    - evaluate(): Evaluate model performance
    - save_model(): Save trained model to file
    """
```

## Adding New Features

### Adding a New Detection Method

To add a new detection method (e.g., yawning detection):

1. **Extend the model class**:

```python
def _detect_yawning(self, landmarks):
    """
    Detect yawning based on mouth landmarks
    
    Args:
        landmarks: Facial landmarks from MediaPipe
        
    Returns:
        bool: True if yawning detected
    """
    # Extract mouth landmarks
    mouth_landmarks = [landmarks[i] for i in self.MOUTH_INDICES]
    
    # Calculate mouth aspect ratio (similar to EAR)
    mar = self._calculate_mouth_aspect_ratio(mouth_landmarks)
    
    # Return true if MAR exceeds threshold
    return mar > self.YAWNING_THRESHOLD
```

2. **Update the process_frame method**:

```python
def process_frame(self, frame):
    # Existing code...
    
    # Add new detection
    is_yawning = False
    if face_landmarks is not None:
        is_yawning = self._detect_yawning(face_landmarks)
    
    # Update results dictionary
    results = {
        # Existing fields...
        'yawning': is_yawning
    }
    
    return results
```

3. **Update the UI to display the new detection**:

```python
def update_status_indicators(self):
    # Existing code...
    
    # Add yawning indicator
    if self.detection_results.get('yawning', False):
        self.yawning_label.setText("Yawning: YES")
        self.yawning_label.setStyleSheet("color: red;")
    else:
        self.yawning_label.setText("Yawning: NO")
        self.yawning_label.setStyleSheet("color: green;")
```

### Creating a New Model

To implement a completely new detection model:

1. **Create a new file** in the `models/` directory:

```python
# models/advanced_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

class AdvancedSafetyModel:
    """
    Advanced model for driver state detection using deep learning
    """
    
    def __init__(self, **kwargs):
        """Initialize model with parameters"""
        self.model = self._create_model()
        # ...
    
    def _create_model(self):
        """Create and compile model architecture"""
        # ...
    
    def process_frame(self, frame):
        """Process frame and return detection results"""
        # Detection logic
        # ...
        
        # Return results in same format as SimpleSafetyModel
        # for compatibility with existing UI
        return results
```

2. **Update `main.py` to support the new model**:

```python
def initialize_model(model_type, **kwargs):
    """Initialize model based on type"""
    if model_type == 'simple':
        from models.simple_model import SimpleSafetyModel
        return SimpleSafetyModel(**kwargs)
    elif model_type == 'advanced':
        from models.advanced_model import AdvancedSafetyModel
        return AdvancedSafetyModel(**kwargs)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
```

3. **Add command line support**:

```python
parser.add_argument('--model_type', type=str, default='simple',
                    choices=['simple', 'advanced'],
                    help='Type of detection model to use')
```

## Model Training and Evaluation

### Training a New Model

To train a custom model:

1. **Collect data** using the data collection tool:

```bash
python main.py --mode collect_data --data_class focused --samples 200
python main.py --mode collect_data --data_class distracted --samples 200
python main.py --mode collect_data --data_class drowsy --samples 200
```

2. **Create a training script** or use the existing ones:

```python
from training.simple_train import SimpleModelTrainer

# Initialize trainer
trainer = SimpleModelTrainer(
    data_dir='data',
    test_size=0.2,
    random_state=42
)

# Load and process data
X_train, X_test, y_train, y_test = trainer.load_and_preprocess_data()

# Train model
model = trainer.train(X_train, y_train)

# Evaluate model
accuracy, precision, recall, f1 = trainer.evaluate(model, X_test, y_test)
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Save model
trainer.save_model('models/my_custom_model.pkl')
```

3. **Use the trained model** in the application:

```bash
python main.py --mode ui --model_path models/my_custom_model.pkl
```

### Model Evaluation

To properly evaluate your models:

```python
def evaluate_model(model_path, test_data_dir):
    """Evaluate a model on test data"""
    # Load model
    model = SimpleSafetyModel()
    model.load_model(model_path)
    
    # Load test data
    test_frames, test_labels = load_test_data(test_data_dir)
    
    # Evaluate
    results = []
    for frame, true_label in zip(test_frames, test_labels):
        detection = model.process_frame(frame)
        predicted_label = 'drowsy' if detection['drowsy'] else 'distracted' if detection['distracted'] else 'focused'
        results.append((true_label, predicted_label))
    
    # Calculate metrics
    accuracy, confusion_matrix = calculate_metrics(results)
    
    # Display results
    print(f"Accuracy: {accuracy:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix)
    
    # Optional: Plot ROC curve, precision-recall curve, etc.
```

## Integration Points

### Integrating with External Systems

The system provides several integration points:

1. **API Mode**:
   - Use `--mode api` to start the system as an API server
   - Receive detection results via HTTP endpoints

2. **Event Hooks**:
   - Register callbacks for detection events
   - Example:
   
   ```python
   def on_drowsiness_detected(detection_data):
       # Custom action when drowsiness is detected
       external_system.send_alert(detection_data)
   
   # Register callback
   model.register_callback('drowsy', on_drowsiness_detected)
   ```

3. **Output Files**:
   - Configure the system to write detection logs to a file
   - Other applications can monitor this file for events
   
   ```json
   "logging": {
     "enabled": true,
     "file": "logs/detections.json",
     "format": "json"
   }
   ```

### Embedding in Other Applications

To use the detection functionality in another application:

```python
from models.simple_model import SimpleSafetyModel

class YourApplication:
    def __init__(self):
        # Initialize the detection model
        self.detection_model = SimpleSafetyModel(
            eye_aspect_ratio_threshold=0.2,
            confidence_threshold=0.7
        )
        self.detection_model.load_model('models/saved_model.pkl')
        
    def process_video_frame(self, frame):
        # Get detection results
        results = self.detection_model.process_frame(frame)
        
        # Use results in your application
        if results['drowsy']:
            self.handle_drowsy_driver()
        elif results['distracted']:
            self.handle_distracted_driver()
```

## Best Practices

### Code Style

Follow these guidelines for code consistency:

- Use PEP 8 style guidelines
- Document all functions and classes with docstrings
- Add type hints where appropriate
- Write unit tests for new functionality

### Performance Optimization

When working with real-time video processing:

1. **Optimize Frame Processing**:
   - Resize frames to the minimum viable size
   - Process every nth frame if full FPS isn't required
   - Use threading to parallelize detection and display

2. **Model Optimization**:
   - Consider quantized models for lower CPU usage
   - Profile your code to identify bottlenecks
   - Implement caching for expensive calculations

3. **Memory Management**:
   - Release resources properly when not in use
   - Monitor memory usage during long running sessions
   - Implement proper cleanup in event handlers

### Testing

Always test new features thoroughly:

1. **Unit Testing**:
   - Write tests for individual components
   - Example:
   
   ```python
   def test_ear_calculation():
       model = SimpleSafetyModel()
       landmarks = create_test_landmarks()
       ear = model._calculate_improved_ear(
           landmarks, model.LEFT_EYE_INDICES, model.RIGHT_EYE_INDICES
       )
       assert 0.15 < ear < 0.4
   ```

2. **Integration Testing**:
   - Test how components work together
   - Verify UI updates correctly based on model results

3. **Performance Testing**:
   - Measure and verify FPS
   - Test on target hardware
   - Ensure consistent performance over time
