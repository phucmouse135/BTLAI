# Driver Drowsiness and Distraction Detection System

## Overview
This system implements a real-time driver monitoring solution to detect drowsiness and distraction states. Using computer vision and machine learning techniques, it analyzes the driver's face, eye state, head position, and hand position to identify potentially unsafe behavior. When detected, the system issues audio and visual alerts to help prevent accidents caused by fatigue or lack of attention.

## Key Features
- Real-time driver drowsiness detection through eye state monitoring
- Distraction detection by tracking head and hand positions
- Customizable alert system with continuous alerts until safe driving is resumed
- User-friendly interface for monitoring and configuration
- Data collection tools for training personalized models
- Violation history tracking for safety analysis

## Documentation
- [Code Explanation](docs/code_explanation.md) - Detailed explanation of algorithms, functions, and formulas
- [User Guide](docs/user_guide.md) - Instructions for using the application
- [Developer Guide](docs/developer_guide.md) - Information for developers extending the system

## Technologies and Libraries

### Computer Vision and Machine Learning
- **OpenCV**: Image processing and basic face detection
- **MediaPipe**: Face landmark detection (468 points) and hand tracking (21 points per hand)
- **scikit-learn**: SVM classification model
- **NumPy**: High-performance numerical computations

### User Interface and Sound
- **PyQt5**: Graphical user interface framework
- **PyAudio**: Audio alert playback

## Project Structure

```
drowsiness_detection/
│
├── assets/             # Static resources for the application
│   └── sounds/         # Alert sound files
│
├── config/             # Configuration files
│
├── data/               # Training data and data collection
│   ├── collect_data.py # Tool for collecting training data
│   ├── distracted/     # Data for distracted driver state
│   ├── eye_state/      # Data for various eye states
│   └── focused/        # Data for focused driver state
│
├── docs/               # Documentation
│   ├── code_explanation.md     # Detailed code and algorithm explanations
│   ├── user_guide.md           # User guide
│   └── developer_guide.md      # Developer guide
│
├── models/             # Model definitions
│   ├── detection_model.py      # TensorFlow-based model
│   ├── simple_model.py         # Lightweight SVM model
│   ├── saved_model.pkl         # Trained model weights
│   └── opencv_face_detector_uint8.pb  # Face detection model
│
├── training/           # Model training scripts
│   ├── simple_train.py  # SVM model training script
│   └── train_model.py   # TensorFlow model training script
│
├── ui/                 # User interfaces
│   └── monitoring_app.py # Driver monitoring UI
│
├── utils/              # Utility functions
│   └── helpers.py      # Helper functions for camera, annotations, etc.
│
├── main.py             # Main entry point for the application
├── requirements.txt    # Python dependencies
└── retrain_model.py    # Script to retrain the model with new data
```

## Core Features

### 1. Detection Model (`models/simple_model.py`)

Uses an SVM (Support Vector Machine) model combined with these features:
- **Eye Aspect Ratio (EAR)**: Calculates the openness of eyes to detect drowsiness
- **Head position analysis**: Detects if the head is turned or tilted
- **Hand position detection**: Determines if hands are placed on the steering wheel

Detection pipeline:
1. Face detection in the video frame
2. Detection of 468 facial landmarks using MediaPipe Face Mesh
3. EAR calculation based on eye landmarks
4. Head position analysis based on facial landmarks
5. Hand position detection using MediaPipe Hands
6. Combination of all information to determine driver's state

### 2. Monitoring Interface (`ui/monitoring_app.py`)

User interface built with PyQt5 featuring:
- Real-time video stream display
- Driver status notifications (OK/Drowsy/Distracted)
- Display of metrics: EAR, head position, hand position
- Sensitivity settings (EAR threshold, confidence threshold)
- Sound alerts when dangerous states are detected
- Save and load user configurations

### 3. Data Collection (`data/collect_data.py`)

Training data collection tool that includes:
- Driver face image capture via webcam
- Automatic classification of eye state, head, and hand positions
- Saving of images and metadata (JSON) for training

### 4. Model Training (`training/simple_train.py`)

SVM model training pipeline:
1. Load and preprocess data from the data/ directory
2. Extract features (EAR, head position, hand position)
3. Normalize features
4. Train SVM model
5. Evaluate performance with test set
6. Save trained model

## Usage Instructions

### Running the Monitoring Application

```bash
python main.py --mode ui
```

### Collecting Training Data

```bash
python main.py --mode collect_data --data_class focused --samples 200
python main.py --mode collect_data --data_class distracted --samples 200
```

### Training the Model

```bash
python main.py --mode train
```

or

```bash
python retrain_model.py
```

## Key Detection Features

### 1. Drowsiness Detection
- Calculates Eye Aspect Ratio (EAR) from eye landmarks
- Compares against threshold (default 0.2)
- Detects prolonged eye closure

### 2. Distraction Detection
- Analyzes head position (turned to side, tilted)
- Determines hand position (not on steering wheel)
- Combines factors to assess distraction level

## Mathematical Foundation

### Eye Aspect Ratio (EAR) Formula

The core drowsiness detection relies on the Eye Aspect Ratio, calculated as:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Where p1 to p6 are specific landmarks around the eye, and ||p1-p4|| represents the Euclidean distance between points p1 and p4.

## Testing Methodology

The system employs a comprehensive testing strategy:

1. **Unit Testing**: Testing individual components in isolation
2. **Integration Testing**: Testing how components work together
3. **Performance Testing**: Ensuring real-time operation capability
4. **Multi-condition Testing**: Testing under various lighting and user conditions
5. **Regression Testing**: Ensuring new changes don't break existing functionality

## Future Development Directions

1. **Microservices Architecture**: Splitting the system into smaller, specialized services
2. **Event-Based Architecture**: Implementing a publish-subscribe pattern for better decoupling
3. **Advanced Deep Learning**: Implementing temporal models (LSTM/RNN) for better sequence analysis
4. **Edge-Cloud Hybrid**: Distributing processing between edge devices and cloud infrastructure

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The EAR calculation is based on the work of Soukupová and Čech (2016)
- MediaPipe team for their excellent vision libraries
- Contributors and testers who helped improve the system
