# Drowsiness Detection System: User Guide

This guide provides instructions for installing, configuring, and using the Drowsiness Detection System.

## Table of Contents
- [Installation](#installation)
- [Running the System](#running-the-system)
- [User Interface](#user-interface)
- [Configuration Options](#configuration-options)
- [Alerts and Notifications](#alerts-and-notifications)
- [Troubleshooting](#troubleshooting)
- [Frequently Asked Questions](#frequently-asked-questions)

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or compatible camera
- Windows, macOS, or Linux operating system

### Steps

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python main.py --check
   ```

## Running the System

### Starting the Monitoring Application

To start the main driver monitoring application:

```bash
python main.py --mode ui
```

This launches the real-time monitoring interface.

### Command Line Options

The system supports various command line options:

```bash
python main.py --mode [ui|collect_data|train] [--options]
```

- `--mode ui`: Start the monitoring UI (default)
- `--mode collect_data`: Launch the data collection tool
- `--mode train`: Train the model with collected data

Additional options:
- `--camera_id [number]`: Specify camera ID (default: 0)
- `--ear_threshold [value]`: Set Eye Aspect Ratio threshold (default: 0.2)
- `--confidence [value]`: Set confidence threshold (default: 0.6)

Examples:
```bash
# Start UI with camera 1
python main.py --mode ui --camera_id 1

# Collect training data for 'focused' state
python main.py --mode collect_data --data_class focused --samples 200

# Train model with custom settings
python main.py --mode train --test_size 0.3 --kernel rbf
```

## User Interface

The monitoring interface consists of several key components:

![UI Overview](assets/images/ui_overview.png)

### Main Elements

1. **Video Display**
   - Shows the camera feed with real-time annotations
   - Facial landmarks and detection results are overlaid

2. **Status Panel**
   - Current driver state: OK, DROWSY, or DISTRACTED
   - EAR value and threshold
   - Head position indicator
   - Hand position status

3. **Control Panel**
   - Camera selection dropdown
   - Sensitivity adjustment sliders
   - Sound alert toggle
   - Settings save/load buttons

4. **Metrics Panel**
   - Real-time metrics display
   - Detection confidence values
   - FPS (Frames Per Second) counter

### Interface Controls

- **Start/Stop Button**: Controls the monitoring process
- **EAR Threshold Slider**: Adjusts sensitivity for drowsiness detection
- **Confidence Slider**: Adjusts detection confidence threshold
- **Sound Toggle**: Enables/disables audio alerts
- **Settings Button**: Opens settings dialog for advanced configuration
- **Export Button**: Exports detection logs and statistics

## Configuration Options

### Basic Configuration

The basic configuration can be adjusted directly in the UI:

| Setting | Description | Default | Range |
|---------|-------------|---------|-------|
| EAR Threshold | Eye Aspect Ratio threshold for drowsiness detection | 0.2 | 0.15-0.3 |
| Confidence Threshold | Minimum confidence for positive detection | 0.6 | 0.5-0.9 |
| Alert Delay | Seconds before triggering an alert | 2.0 | 0.5-5.0 |
| Camera ID | Camera device ID to use | 0 | System-dependent |

### Advanced Configuration

Advanced settings can be modified through the settings dialog or config file:

- **Detection Parameters**:
  - Face detection confidence
  - Landmark detection quality
  - Temporal smoothing window size

- **Alert Configuration**:
  - Sound file selection
  - Alert frequency
  - Continuous alert duration

- **UI Preferences**:
  - Display metrics visibility
  - Annotation overlay options
  - Theme selection

### Configuration File

You can modify the `config/settings.json` file directly:

```json
{
  "camera": {
    "device_id": 0,
    "width": 640,
    "height": 480,
    "fps": 30
  },
  "detection": {
    "ear_threshold": 0.2,
    "confidence_threshold": 0.6,
    "consecutive_frames": 3,
    "head_turned_threshold": 0.3,
    "head_tilted_threshold": 0.2
  },
  "alerts": {
    "sound_enabled": true,
    "drowsy_sound": "assets/sounds/drowsy_alert.wav",
    "distracted_sound": "assets/sounds/distracted_alert.wav",
    "continuous_alerts": true,
    "alert_interval": 3.0
  },
  "ui": {
    "show_landmarks": true,
    "show_fps": true,
    "show_metrics": true
  }
}
```

## Alerts and Notifications

The system provides several types of alerts:

### Visual Alerts

- **Status Indicator**: Changes color based on detected state
  - Green: Normal/OK
  - Yellow: Warning
  - Red: Alert (Drowsy or Distracted)

- **On-screen Messages**: Text alerts describing the detected issue

### Audio Alerts

- **Drowsiness Alert**: Played when driver appears drowsy
- **Distraction Alert**: Played when driver appears distracted
- **Continuous Alerts**: Repeated until the driver returns to a safe state

### Alert Customization

1. **Changing Alert Sounds**
   - Replace sound files in the `assets/sounds/` directory
   - Use the settings dialog to select different sound files

2. **Alert Sensitivity**
   - Adjust thresholds for fewer/more frequent alerts
   - Modify consecutive frame settings for faster/slower response

## Troubleshooting

### Common Issues and Solutions

| Issue | Possible Causes | Solutions |
|-------|----------------|-----------|
| Camera not detected | Driver issues, hardware problems | Check device connections, reinstall drivers |
| Low FPS | High resolution, CPU limitations | Reduce resolution in settings, close other applications |
| False drowsiness alerts | Poor lighting, EAR threshold too high | Improve lighting, lower EAR threshold |
| Face not detected | Poor lighting, face out of frame | Adjust camera position, improve lighting |
| Application crashes | Memory issues, missing dependencies | Restart application, reinstall dependencies |

### Performance Optimization

If the system is running slowly:

1. **Reduce Resolution**:
   ```json
   "camera": {
     "width": 320,
     "height": 240
   }
   ```

2. **Lower Processing Quality**:
   ```json
   "detection": {
     "landmark_quality": "fast"
   }
   ```

3. **Disable Features**:
   ```json
   "ui": {
     "show_landmarks": false,
     "show_metrics": false
   }
   ```

### Error Logs

Error logs are stored in the `logs/` directory. These can be helpful when reporting issues.

## Frequently Asked Questions

### General Questions

**Q: How accurate is the drowsiness detection?**  
A: The system achieves approximately 90% accuracy in typical conditions. Accuracy depends on lighting, camera quality, and user calibration.

**Q: Can the system work at night?**  
A: Yes, but adequate IR illumination or cabin lighting is required for the camera to see the driver's face properly.

**Q: How much CPU does the application use?**  
A: The SVM-based model typically uses 20-30% CPU on a modern computer. The CNN model may require more resources.

### Technical Questions

**Q: Can I use a custom model?**  
A: Yes, you can train custom models with `retrain_model.py` and your own dataset.

**Q: How do I collect my own training data?**  
A: Use the data collection mode:
```bash
python main.py --mode collect_data --data_class [state] --samples [number]
```

**Q: Can the system integrate with other applications?**  
A: Yes, you can use the API provided in `utils/helpers.py` to integrate with other systems.

### Usage Questions

**Q: Should I wear glasses while using the system?**  
A: The system works with most glasses, but very reflective or tinted glasses may reduce accuracy.

**Q: How do I calibrate the system for my face?**  
A: The system automatically adapts, but for best results, collect some training data in your typical driving position.
