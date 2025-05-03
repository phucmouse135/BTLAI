import sys
import os
import cv2
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QComboBox, 
                            QSlider, QCheckBox, QGroupBox, QRadioButton, 
                            QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox,
                            QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QUrl, QDateTime
from PyQt5.QtGui import QImage, QPixmap, QColor
# Import sound functionality
from PyQt5.QtMultimedia import QSound

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the simplified model instead of the TensorFlow-based one
from models.simple_model import SimpleSafetyModel
from utils.helpers import initialize_camera, annotate_frame, calculate_fps, save_config, load_config

class DriverMonitoringUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        'config', 'settings.json')
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        self.config = load_config(self.config_path)
        
        # Set default configuration if not loaded
        if not self.config:
            self.config = {
                'camera_id': 0,
                'ear_threshold': 0.2,
                'confidence_threshold': 0.7,
                'detection_mode': 'all',
                'frame_rate': 15,
                'model_path': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                          'models', 'saved_model.pkl'),
                'capture_width': 640,
                'capture_height': 480,
                'sound_alerts_enabled': True,  # Add sound alert setting
                'continuous_alerts': True      # Add continuous alert setting
            }
        
        # Initialize sound alert variables
        self.sound_alerts_enabled = self.config.get('sound_alerts_enabled', True)
        self.continuous_alerts = self.config.get('continuous_alerts', True)
        self.drowsy_sound_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                             'assets', 'sounds', 'drowsy_alert.wav')
        self.distracted_sound_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                 'assets', 'sounds', 'distracted_alert.wav')
        self.ensure_sound_files_exist()
        
        # Track alert states to prevent continuous alerts
        self.drowsy_alert_active = False
        self.distracted_alert_active = False
        self.alert_cooldown = 3.0  # seconds between alerts
        self.last_drowsy_alert_time = 0
        self.last_distracted_alert_time = 0
        
        # New sound timers for continuous alerts
        self.drowsy_sound_timer = QTimer()
        self.drowsy_sound_timer.timeout.connect(lambda: self.play_alert_sound('drowsy', True))
        self.drowsy_sound_timer.setInterval(3000)  # Play sound every 3 seconds
        
        self.distracted_sound_timer = QTimer()
        self.distracted_sound_timer.timeout.connect(lambda: self.play_alert_sound('distracted', True))
        self.distracted_sound_timer.setInterval(3000)  # Play sound every 3 seconds
        
        # Initialize violation history tracking
        self.violation_history = []
        self.max_history_entries = 100  # Maximum number of violations to track
        
        # Initialize model
        self.model = None
        self.model_loaded = False
        self.load_model()
        
        # Initialize camera
        self.camera = None
        self.is_camera_running = False
        
        # FPS calculation
        self.fps_counter = calculate_fps()
        
        # Initialize UI
        self.setWindowTitle("Driver Safety Monitoring System")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Setup UI components
        self._setup_camera_view()
        self._setup_controls()
        self._setup_violation_history()
        
        # Setup timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        # Show the UI
        self.show()
        
    def _setup_camera_view(self):
        """Setup the camera view area"""
        # Create camera view container
        self.camera_container = QWidget()
        self.camera_layout = QVBoxLayout(self.camera_container)
        
        # Camera feed display
        self.camera_label = QLabel("Camera feed will appear here")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: black; color: white;")
        self.camera_label.setMinimumSize(640, 480)
        
        # Status bar beneath camera
        self.status_widget = QWidget()
        self.status_layout = QHBoxLayout(self.status_widget)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        
        # Status indicators
        self.drowsy_indicator = QLabel("DROWSY: NO")
        self.drowsy_indicator.setStyleSheet("color: green;")
        
        self.distracted_indicator = QLabel("DISTRACTED: NO")
        self.distracted_indicator.setStyleSheet("color: green;")
        
        self.fps_label = QLabel("FPS: 0")
        
        # Add indicators to status layout
        self.status_layout.addWidget(self.drowsy_indicator)
        self.status_layout.addWidget(self.distracted_indicator)
        self.status_layout.addWidget(self.fps_label)
        
        # Add widgets to camera layout
        self.camera_layout.addWidget(self.camera_label)
        self.camera_layout.addWidget(self.status_widget)
        
        # Add camera container to main layout (70% of width)
        self.main_layout.addWidget(self.camera_container, 7)

    def ensure_sound_files_exist(self):
        """Create default sound files if they don't exist"""
        # Create sound directory if it doesn't exist
        sound_dir = os.path.dirname(self.drowsy_sound_path)
        os.makedirs(sound_dir, exist_ok=True)
        
        # Check if drowsy alert sound exists, create a default one if not
        if not os.path.exists(self.drowsy_sound_path):
            try:
                # Look for system sound files first
                system_sounds = [
                    r"C:\Windows\Media\Windows Exclamation.wav",
                    r"C:\Windows\Media\Windows Critical Stop.wav",
                    r"C:\Windows\Media\Alarm01.wav",
                    r"C:\Windows\Media\Alarm02.wav",
                    r"C:\Windows\Media\Alarm03.wav"
                ]
                
                sound_found = False
                for system_sound in system_sounds:
                    if os.path.exists(system_sound):
                        # Copy system sound to our directory
                        import shutil
                        shutil.copy(system_sound, self.drowsy_sound_path)
                        sound_found = True
                        break
                
                if not sound_found:
                    # If no system sounds found, create a simple one
                    self.create_simple_beep_sound(self.drowsy_sound_path)
            except Exception as e:
                print(f"Error creating drowsy alert sound: {e}")
        
        # Check if distracted alert sound exists, create a default one if not
        if not os.path.exists(self.distracted_sound_path):
            try:
                # Look for a different system sound
                system_sounds = [
                    r"C:\Windows\Media\Windows Notify.wav",
                    r"C:\Windows\Media\Notify.wav",
                    r"C:\Windows\Media\Ring05.wav",
                    r"C:\Windows\Media\Ring06.wav"
                ]
                
                sound_found = False
                for system_sound in system_sounds:
                    if os.path.exists(system_sound):
                        # Copy system sound to our directory
                        import shutil
                        shutil.copy(system_sound, self.distracted_sound_path)
                        sound_found = True
                        break
                
                if not sound_found and os.path.exists(self.drowsy_sound_path):
                    # If no system sounds found, copy drowsy sound
                    import shutil
                    shutil.copy(self.drowsy_sound_path, self.distracted_sound_path)
                elif not sound_found:
                    # Create a different simple sound
                    self.create_simple_beep_sound(self.distracted_sound_path, frequency=800)
            except Exception as e:
                print(f"Error creating distracted alert sound: {e}")
    
    def create_simple_beep_sound(self, filepath, frequency=440, duration=0.75):
        """Create a simple WAV file with a beep sound"""
        try:
            import wave
            import struct
            import math
            
            # Audio parameters
            sample_rate = 44100
            num_samples = int(sample_rate * duration)
            
            with wave.open(filepath, 'w') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Generate sine wave
                for i in range(num_samples):
                    sample = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
                    wav_file.writeframes(struct.pack('h', sample))
        except Exception as e:
            print(f"Error creating beep sound: {e}")
            
            # Try a simpler approach as fallback
            try:
                # Create a very simple WAV file (1 second of silence)
                with open(filepath, 'wb') as f:
                    # Write WAV header
                    f.write(b'RIFF')
                    f.write((36).to_bytes(4, 'little'))  # File size - 8
                    f.write(b'WAVE')
                    f.write(b'fmt ')
                    f.write((16).to_bytes(4, 'little'))  # Size of fmt chunk
                    f.write((1).to_bytes(2, 'little'))   # PCM format
                    f.write((1).to_bytes(2, 'little'))   # Mono
                    f.write((44100).to_bytes(4, 'little'))  # Sample rate
                    f.write((44100 * 2).to_bytes(4, 'little'))  # Byte rate
                    f.write((2).to_bytes(2, 'little'))   # Block align
                    f.write((16).to_bytes(2, 'little'))  # Bits per sample
                    f.write(b'data')
                    f.write((44100 * 2).to_bytes(4, 'little'))  # Data size
                    # Write 1 second of silence
                    f.write(b'\x00' * 44100 * 2)
            except Exception as e:
                print(f"Error creating fallback sound file: {e}")
                
    def play_alert_sound(self, alert_type, from_timer=False):
        """Play an alert sound based on the type of detection"""
        if not self.sound_alerts_enabled:
            return
        
        # For non-timer calls, manage the continuous alert timers
        if not from_timer:
            if alert_type == 'drowsy' and self.continuous_alerts:
                # If not already running, start the timer
                if not self.drowsy_sound_timer.isActive():
                    self.drowsy_sound_timer.start()
            elif alert_type == 'distracted' and self.continuous_alerts:
                # If not already running, start the timer
                if not self.distracted_sound_timer.isActive():
                    self.distracted_sound_timer.start()
        
        # Play the actual sound
        current_time = self.fps_counter.get_elapsed_time()
        
        if alert_type == 'drowsy':
            # For regular alerts, check cooldown
            if not from_timer and current_time - self.last_drowsy_alert_time < self.alert_cooldown:
                return
                
            if os.path.exists(self.drowsy_sound_path):
                QSound.play(self.drowsy_sound_path)
                self.last_drowsy_alert_time = current_time
                
        elif alert_type == 'distracted':
            # For regular alerts, check cooldown
            if not from_timer and current_time - self.last_distracted_alert_time < self.alert_cooldown:
                return
                
            if os.path.exists(self.distracted_sound_path):
                QSound.play(self.distracted_sound_path)
                self.last_distracted_alert_time = current_time
    
    def load_model(self):
        """Load the detection model"""
        try:
            model_path = self.config.get('model_path', None)
            
            # Use our simplified model instead
            self.model = SimpleSafetyModel(
                eye_aspect_ratio_threshold=self.config.get('ear_threshold', 0.2),
                confidence_threshold=self.config.get('confidence_threshold', 0.7),
                model_path=model_path if (model_path and os.path.exists(model_path)) else None
            )
            
            self.model_loaded = True
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model: {str(e)}")
            self.model_loaded = False
            return False
        
    def _setup_controls(self):
        """Setup the control panel area"""
        # Create controls container (30% of width)
        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_container)
        self.main_layout.addWidget(self.controls_container, 3)
        
        # Camera controls group
        self.camera_group = QGroupBox("Camera Controls")
        self.camera_group_layout = QVBoxLayout()
        
        # Camera selection
        camera_select_layout = QHBoxLayout()
        camera_select_layout.addWidget(QLabel("Camera:"))
        self.camera_select = QComboBox()
        self.camera_select.addItems([f"Camera {i}" for i in range(3)])  # Add 3 camera options
        self.camera_select.setCurrentIndex(self.config.get('camera_id', 0))
        camera_select_layout.addWidget(self.camera_select)
        
        # Camera start/stop buttons
        self.camera_button_layout = QHBoxLayout()
        self.start_camera_btn = QPushButton("Start Camera")
        self.start_camera_btn.clicked.connect(self.start_camera)
        self.stop_camera_btn = QPushButton("Stop Camera")
        self.stop_camera_btn.clicked.connect(self.stop_camera)
        self.stop_camera_btn.setEnabled(False)
        self.camera_button_layout.addWidget(self.start_camera_btn)
        self.camera_button_layout.addWidget(self.stop_camera_btn)
        
        # Add to camera group
        self.camera_group_layout.addLayout(camera_select_layout)
        self.camera_group_layout.addLayout(self.camera_button_layout)
        self.camera_group.setLayout(self.camera_group_layout)
        
        # Detection Settings group
        self.settings_group = QGroupBox("Detection Settings")
        self.settings_group_layout = QVBoxLayout()
        
        # Detection mode
        self.mode_layout = QVBoxLayout()
        self.mode_layout.addWidget(QLabel("Detection Mode:"))
        
        self.mode_all = QRadioButton("All Features")
        self.mode_drowsy = QRadioButton("Drowsiness Only")
        self.mode_distraction = QRadioButton("Distraction Only")
        
        # Set default based on config
        mode = self.config.get('detection_mode', 'all')
        if mode == 'drowsy':
            self.mode_drowsy.setChecked(True)
        elif mode == 'distraction':
            self.mode_distraction.setChecked(True)
        else:
            self.mode_all.setChecked(True)
        
        # Connect signals
        self.mode_all.toggled.connect(lambda: self.update_detection_mode('all'))
        self.mode_drowsy.toggled.connect(lambda: self.update_detection_mode('drowsy'))
        self.mode_distraction.toggled.connect(lambda: self.update_detection_mode('distraction'))
        
        self.mode_layout.addWidget(self.mode_all)
        self.mode_layout.addWidget(self.mode_drowsy)
        self.mode_layout.addWidget(self.mode_distraction)
        
        # Sound Alerts Checkbox
        self.sound_alerts_checkbox = QCheckBox("Enable Sound Alerts")
        self.sound_alerts_checkbox.setChecked(self.sound_alerts_enabled)
        self.sound_alerts_checkbox.toggled.connect(self.toggle_sound_alerts)
        self.mode_layout.addWidget(self.sound_alerts_checkbox)
        
        # Continuous Alerts Checkbox
        self.continuous_alerts_checkbox = QCheckBox("Continuous Alerts Until Safe")
        self.continuous_alerts_checkbox.setChecked(self.continuous_alerts)
        self.continuous_alerts_checkbox.toggled.connect(self.toggle_continuous_alerts)
        self.mode_layout.addWidget(self.continuous_alerts_checkbox)
        
        # EAR Threshold slider
        self.ear_layout = QVBoxLayout()
        ear_label_layout = QHBoxLayout()
        ear_label_layout.addWidget(QLabel("Eye Aspect Ratio Threshold:"))
        self.ear_value_label = QLabel(f"{self.config.get('ear_threshold', 0.2):.2f}")
        ear_label_layout.addWidget(self.ear_value_label)
        self.ear_layout.addLayout(ear_label_layout)
        
        self.ear_slider = QSlider(Qt.Horizontal)
        self.ear_slider.setRange(5, 40)  # Values from 0.05 to 0.40
        self.ear_slider.setValue(int(self.config.get('ear_threshold', 0.2) * 100))
        self.ear_slider.setTickPosition(QSlider.TicksBelow)
        self.ear_slider.setTickInterval(5)
        self.ear_slider.valueChanged.connect(self.update_ear_threshold)
        self.ear_layout.addWidget(self.ear_slider)
        
        # Confidence threshold slider
        self.conf_layout = QVBoxLayout()
        conf_label_layout = QHBoxLayout()
        conf_label_layout.addWidget(QLabel("Confidence Threshold:"))
        self.conf_value_label = QLabel(f"{self.config.get('confidence_threshold', 0.7):.2f}")
        conf_label_layout.addWidget(self.conf_value_label)
        self.conf_layout.addLayout(conf_label_layout)
        
        self.conf_slider = QSlider(Qt.Horizontal)
        self.conf_slider.setRange(30, 95)  # Values from 0.30 to 0.95
        self.conf_slider.setValue(int(self.config.get('confidence_threshold', 0.7) * 100))
        self.conf_slider.setTickPosition(QSlider.TicksBelow)
        self.conf_slider.setTickInterval(5)
        self.conf_slider.valueChanged.connect(self.update_conf_threshold)
        self.conf_layout.addWidget(self.conf_slider)
        
        # Performance Settings
        self.perf_layout = QVBoxLayout()
        self.perf_layout.addWidget(QLabel("Performance Settings:"))
        
        # Frame rate control
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("Frame Rate:"))
        self.fps_spinner = QSpinBox()
        self.fps_spinner.setRange(1, 30)
        self.fps_spinner.setValue(self.config.get('frame_rate', 15))
        self.fps_spinner.valueChanged.connect(self.update_frame_rate)
        fps_layout.addWidget(self.fps_spinner)
        self.perf_layout.addLayout(fps_layout)
        
        # Add to settings group
        self.settings_group_layout.addLayout(self.mode_layout)
        self.settings_group_layout.addLayout(self.ear_layout)
        self.settings_group_layout.addLayout(self.conf_layout)
        self.settings_group_layout.addLayout(self.perf_layout)
        self.settings_group.setLayout(self.settings_group_layout)
        
        # Sound Controls group
        self.sound_group = QGroupBox("Alert Sound Settings")
        self.sound_group_layout = QVBoxLayout()
        
        # Drowsy sound selection
        self.drowsy_sound_btn = QPushButton("Select Drowsy Alert Sound...")
        self.drowsy_sound_btn.clicked.connect(lambda: self.select_alert_sound('drowsy'))
        self.sound_group_layout.addWidget(self.drowsy_sound_btn)
        
        # Distracted sound selection
        self.distracted_sound_btn = QPushButton("Select Distracted Alert Sound...")
        self.distracted_sound_btn.clicked.connect(lambda: self.select_alert_sound('distracted'))
        self.sound_group_layout.addWidget(self.distracted_sound_btn)
        
        # Test sound buttons
        test_sound_layout = QHBoxLayout()
        self.test_drowsy_btn = QPushButton("Test Drowsy Sound")
        self.test_drowsy_btn.clicked.connect(lambda: self.play_alert_sound('drowsy'))
        
        self.test_distracted_btn = QPushButton("Test Distracted Sound")
        self.test_distracted_btn.clicked.connect(lambda: self.play_alert_sound('distracted'))
        
        test_sound_layout.addWidget(self.test_drowsy_btn)
        test_sound_layout.addWidget(self.test_distracted_btn)
        self.sound_group_layout.addLayout(test_sound_layout)
        
        self.sound_group.setLayout(self.sound_group_layout)
        
        # Model Management group
        self.model_group = QGroupBox("Model Management")
        self.model_group_layout = QVBoxLayout()
        
        # Load different model button
        self.load_model_btn = QPushButton("Load Model...")
        self.load_model_btn.clicked.connect(self.on_load_model)
        
        # Save configuration button
        self.save_config_btn = QPushButton("Save Configuration")
        self.save_config_btn.clicked.connect(self.save_configuration)
        
        # Add to model group
        self.model_group_layout.addWidget(self.load_model_btn)
        self.model_group_layout.addWidget(self.save_config_btn)
        self.model_group.setLayout(self.model_group_layout)
        
        # Add all groups to controls layout
        self.controls_layout.addWidget(self.camera_group)
        self.controls_layout.addWidget(self.settings_group)
        self.controls_layout.addWidget(self.sound_group)
        self.controls_layout.addWidget(self.model_group)
        self.controls_layout.addStretch()
        
    def select_alert_sound(self, alert_type):
        """Open file dialog to select a custom alert sound"""
        sound_path, _ = QFileDialog.getOpenFileName(
            self, f"Select {alert_type.capitalize()} Alert Sound", "", "Sound Files (*.wav);;All Files (*)"
        )
        
        if sound_path:
            if alert_type == 'drowsy':
                # Copy the selected sound to our sounds directory
                import shutil
                destination = self.drowsy_sound_path
                try:
                    shutil.copy(sound_path, destination)
                    QMessageBox.information(self, "Success", f"{alert_type.capitalize()} alert sound updated")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to copy sound file: {e}")
            elif alert_type == 'distracted':
                # Copy the selected sound to our sounds directory
                import shutil
                destination = self.distracted_sound_path
                try:
                    shutil.copy(sound_path, destination)
                    QMessageBox.information(self, "Success", f"{alert_type.capitalize()} alert sound updated")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to copy sound file: {e}")
                    
    def toggle_sound_alerts(self, enabled):
        """Enable or disable sound alerts"""
        self.sound_alerts_enabled = enabled
        self.config['sound_alerts_enabled'] = enabled
        
        # If sound alerts are disabled, stop any active alert sounds
        if not enabled:
            self.drowsy_sound_timer.stop()
            self.distracted_sound_timer.stop()
    
    def toggle_continuous_alerts(self, enabled):
        """Enable or disable continuous alerts"""
        self.continuous_alerts = enabled
        self.config['continuous_alerts'] = enabled
        
        # If continuous alerts are disabled, stop any ongoing alert timers
        if not enabled:
            self.drowsy_sound_timer.stop()
            self.distracted_sound_timer.stop()
    
    def update_detection_mode(self, mode):
        """Update the detection mode setting"""
        self.config['detection_mode'] = mode
        
    def update_ear_threshold(self, value):
        """Update the eye aspect ratio threshold"""
        threshold = value / 100.0
        self.ear_value_label.setText(f"{threshold:.2f}")
        self.config['ear_threshold'] = threshold
        
        if self.model_loaded:
            self.model.eye_aspect_ratio_threshold = threshold
            
    def update_conf_threshold(self, value):
        """Update the confidence threshold"""
        threshold = value / 100.0
        self.conf_value_label.setText(f"{threshold:.2f}")
        self.config['confidence_threshold'] = threshold
        
        if self.model_loaded:
            self.model.confidence_threshold = threshold
            
    def update_frame_rate(self, value):
        """Update the frame rate"""
        self.config['frame_rate'] = value
        
        if self.is_camera_running:
            self.timer.setInterval(1000 // value)
            
    def save_configuration(self):
        """Save current configuration to file"""
        if save_config(self.config, self.config_path):
            QMessageBox.information(self, "Success", "Configuration saved successfully")
        else:
            QMessageBox.warning(self, "Warning", "Failed to save configuration")
            
    def on_load_model(self):
        """Handle loading a different model"""
        # Open file dialog with updated filter for pickle files
        model_path, _ = QFileDialog.getOpenFileName(
            self, "Select Model File", "", "Model Files (*.pkl);;All Files (*)"
        )
        
        if model_path:
            # Stop camera if running
            was_running = self.is_camera_running
            if was_running:
                self.stop_camera()
                
            # Update config
            self.config['model_path'] = model_path
            
            # Load new model
            if self.load_model():
                QMessageBox.information(self, "Success", "Model loaded successfully")
                
                # Restart camera if it was running
                if was_running:
                    self.start_camera()
    
    def start_camera(self):
        """Start the camera feed"""
        if self.is_camera_running:
            return
            
        if not self.model_loaded:
            QMessageBox.warning(self, "Warning", "Model not loaded. Basic functionality may be limited.")
        
        # Get camera ID from combobox
        camera_id = self.camera_select.currentIndex()
        
        # Initialize camera
        self.camera = initialize_camera(
            camera_id,
            width=self.config.get('capture_width', 640),
            height=self.config.get('capture_height', 480)
        )
        
        if self.camera is None:
            QMessageBox.critical(self, "Error", f"Failed to open camera {camera_id}")
            return
            
        # Update UI state
        self.start_camera_btn.setEnabled(False)
        self.stop_camera_btn.setEnabled(True)
        self.camera_select.setEnabled(False)
        
        # Start timer for frame updates
        self.timer.start(1000 // self.config.get('frame_rate', 15))
        
        self.is_camera_running = True
    
    def stop_camera(self):
        """Stop the camera feed"""
        if not self.is_camera_running:
            return
            
        # Stop timer
        self.timer.stop()
        
        # Stop alert timers
        self.drowsy_sound_timer.stop()
        self.distracted_sound_timer.stop()
        
        # Release camera
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        # Update UI state
        self.start_camera_btn.setEnabled(True)
        self.stop_camera_btn.setEnabled(False)
        self.camera_select.setEnabled(True)
        
        # Reset camera label
        self.camera_label.setText("Camera feed will appear here")
        self.drowsy_indicator.setText("DROWSY: NO")
        self.distracted_indicator.setText("DISTRACTED: NO")
        self.drowsy_indicator.setStyleSheet("color: green;")
        self.distracted_indicator.setStyleSheet("color: green;")
        
        self.is_camera_running = False
    
    def update_frame(self):
        """Update the camera frame and run detection"""
        if not self.is_camera_running or self.camera is None:
            return
            
        # Read frame from camera
        ret, frame = self.camera.read()
        
        if not ret:
            self.stop_camera()
            QMessageBox.critical(self, "Error", "Failed to capture frame from camera")
            return
            
        # Update FPS counter
        self.fps_counter.update()
        fps = self.fps_counter.get_fps()
        self.fps_label.setText(f"FPS: {fps:.1f}")
        
        # Process frame with model
        detection_mode = self.config.get('detection_mode', 'all')
        
        if self.model_loaded:
            results = self.model.process_frame(frame)
            
            # Filter results based on detection mode
            if detection_mode == 'drowsy':
                results['distracted'] = False
            elif detection_mode == 'distraction':
                results['drowsy'] = False
                
            # Update status indicators
            self.update_status_indicators(results)
            
            # Annotate frame
            frame = annotate_frame(
                frame, 
                results, 
                ear_threshold=self.config.get('ear_threshold', 0.2)
            )
        
        # Convert frame to QImage and display
        self.display_frame(frame)
    
    def display_frame(self, frame):
        """Display a frame in the UI"""
        # Convert the frame to RGB (OpenCV uses BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Resize to fit the label if needed (maintaining aspect ratio)
        q_img = q_img.scaled(self.camera_label.width(), self.camera_label.height(), 
                            Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Display image
        self.camera_label.setPixmap(QPixmap.fromImage(q_img))
    
    def update_status_indicators(self, results):
        """Update the status indicators based on detection results"""
        # Previous state
        was_drowsy = self.drowsy_indicator.text() == "DROWSY: YES"
        was_distracted = self.distracted_indicator.text() == "DISTRACTED: YES"
        
        # Update drowsiness indicator
        if results.get('drowsy', False):
            self.drowsy_indicator.setText("DROWSY: YES")
            self.drowsy_indicator.setStyleSheet("color: red; font-weight: bold;")
            
            # Play alert sound if state changed from not drowsy to drowsy
            if not was_drowsy:
                self.play_alert_sound('drowsy')
                # Record this new violation
                self.record_violation('drowsy', results.get('drowsiness_confidence', 0.8))
        else:
            self.drowsy_indicator.setText("DROWSY: NO")
            self.drowsy_indicator.setStyleSheet("color: green;")
            # Stop continuous drowsy alert if it was active
            if was_drowsy and self.drowsy_sound_timer.isActive():
                self.drowsy_sound_timer.stop()
            
        # Update distraction indicator
        if results.get('distracted', False):
            self.distracted_indicator.setText("DISTRACTED: YES")
            self.distracted_indicator.setStyleSheet("color: red; font-weight: bold;")
            
            # Play alert sound if state changed from not distracted to distracted
            if not was_distracted:
                self.play_alert_sound('distracted')
                # Record this new violation
                self.record_violation('distracted', results.get('distraction_confidence', 0.8))
        else:
            self.distracted_indicator.setText("DISTRACTED: NO")
            self.distracted_indicator.setStyleSheet("color: green;")
            # Stop continuous distracted alert if it was active
            if was_distracted and self.distracted_sound_timer.isActive():
                self.distracted_sound_timer.stop()
    
    def _setup_violation_history(self):
        """Setup the violation history display area below the camera view"""
        # Create a container for the violation history
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        
        # Add a title
        history_title = QLabel("Violation History")
        history_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.history_layout.addWidget(history_title)
        
        # Create table to display violation history
        self.history_table = QTableWidget(0, 4)  # Start with 0 rows, 4 columns
        self.history_table.setHorizontalHeaderLabels(["Time", "Type", "Duration (s)", "Confidence"])
        
        # Set column widths
        self.history_table.setColumnWidth(0, 150)  # Time
        self.history_table.setColumnWidth(1, 100)  # Type
        self.history_table.setColumnWidth(2, 100)  # Duration
        self.history_table.setColumnWidth(3, 100)  # Confidence
        
        # Set table properties
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        
        # Add buttons for violation history management
        button_layout = QHBoxLayout()
        
        self.clear_history_btn = QPushButton("Clear History")
        self.clear_history_btn.clicked.connect(self.clear_violation_history)
        
        self.export_history_btn = QPushButton("Export to CSV...")
        self.export_history_btn.clicked.connect(self.export_violation_history)
        
        button_layout.addWidget(self.clear_history_btn)
        button_layout.addWidget(self.export_history_btn)
        button_layout.addStretch()
        
        # Add to layout
        self.history_layout.addWidget(self.history_table)
        self.history_layout.addLayout(button_layout)
        
        # Add to camera layout (after the camera feed)
        self.camera_layout.addWidget(self.history_container)
    
    def record_violation(self, violation_type, confidence):
        """Record a violation in the history table"""
        # Create a new violation entry
        timestamp = datetime.now()
        
        violation = {
            'time': timestamp,
            'type': violation_type,
            'confidence': confidence,
            'duration': 0  # Initial duration is 0
        }
        
        # Add to violation history (at the beginning)
        self.violation_history.insert(0, violation)
        
        # Limit the history size
        if len(self.violation_history) > self.max_history_entries:
            self.violation_history.pop()
        
        # Update the table
        self.update_violation_history_table()
    
    def update_violation_history_table(self):
        """Update the violation history table with current data"""
        # Clear the table
        self.history_table.setRowCount(0)
        
        # Add violations to table
        for idx, violation in enumerate(self.violation_history):
            self.history_table.insertRow(idx)
            
            # Format time
            time_str = violation['time'].strftime('%Y-%m-%d %H:%M:%S')
            time_item = QTableWidgetItem(time_str)
            
            # Format type (capitalize first letter)
            type_str = violation['type'].capitalize()
            type_item = QTableWidgetItem(type_str)
            
            # Format duration
            duration_str = f"{violation['duration']:.1f}"
            duration_item = QTableWidgetItem(duration_str)
            
            # Format confidence
            confidence_str = f"{violation['confidence']:.2f}"
            confidence_item = QTableWidgetItem(confidence_str)
            
            # Set items in table
            self.history_table.setItem(idx, 0, time_item)
            self.history_table.setItem(idx, 1, type_item)
            self.history_table.setItem(idx, 2, duration_item)
            self.history_table.setItem(idx, 3, confidence_item)
            
            # Set row color based on violation type
            if violation['type'] == 'drowsy':
                time_item.setBackground(QColor(255, 200, 200))  # Light red
                type_item.setBackground(QColor(255, 200, 200))
                duration_item.setBackground(QColor(255, 200, 200))
                confidence_item.setBackground(QColor(255, 200, 200))
            else:  # distracted
                time_item.setBackground(QColor(255, 255, 200))  # Light yellow
                type_item.setBackground(QColor(255, 255, 200))
                duration_item.setBackground(QColor(255, 255, 200))
                confidence_item.setBackground(QColor(255, 255, 200))
                
    def clear_violation_history(self):
        """Clear the violation history"""
        # Confirm with user
        reply = QMessageBox.question(
            self, 
            "Clear Violation History",
            "Are you sure you want to clear the violation history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear the history list
            self.violation_history.clear()
            
            # Update the table
            self.history_table.setRowCount(0)
            
    def export_violation_history(self):
        """Export the violation history to a CSV file"""
        if not self.violation_history:
            QMessageBox.information(
                self,
                "Export Violation History",
                "No violations to export."
            )
            return
            
        # Ask user for file location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Violation History",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled
            
        # Add .csv extension if not present
        if not file_path.lower().endswith('.csv'):
            file_path += '.csv'
            
        try:
            # Write to CSV
            with open(file_path, 'w', newline='') as csvfile:
                import csv
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Time', 'Type', 'Duration (s)', 'Confidence'])
                
                # Write data
                for violation in self.violation_history:
                    writer.writerow([
                        violation['time'].strftime('%Y-%m-%d %H:%M:%S'),
                        violation['type'].capitalize(),
                        f"{violation['duration']:.1f}",
                        f"{violation['confidence']:.2f}"
                    ])
                    
            QMessageBox.information(
                self,
                "Export Successful",
                f"Violation history exported to:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export violation history: {str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    window = DriverMonitoringUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()