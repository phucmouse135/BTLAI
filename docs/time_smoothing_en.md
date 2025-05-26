# Time Smoothing Methods

The system uses multiple time-smoothing methods to improve accuracy and reduce false alerts:

> Note: This is the English version of the document. The Vietnamese version is available at [time_smoothing.md](time_smoothing.md).

## 1. Moving Average Filter

The mathematical formula for the moving average filter applied to EAR values:

```
EAR_smoothed(t) = (1/N) × Σ[EAR(t-i)] for i from 0 to N-1
```

Where:
- `EAR_smoothed(t)` is the smoothed EAR value at time t
- `EAR(t-i)` is the original EAR value at time t-i
- `N` is the size of the sliding window (typically N = 5 to 10 frames)

This filter is implemented in the source code as follows:

```python
# Update EAR value history
self.ear_history.append(ear)
if len(self.ear_history) > self.MAX_EAR_HISTORY:
    self.ear_history.pop(0)
    
# Calculate moving average
if len(self.ear_history) > 0:
    smoothed_ear = sum(self.ear_history) / len(self.ear_history)
else:
    smoothed_ear = ear
```

## 2. Median Filter

Formula for the median filter:

```
EAR_median(t) = median[EAR(t-N+1), EAR(t-N+2), ..., EAR(t)]
```

This filter is particularly effective at removing outlier noise in EAR data. It prioritizes the median value rather than the mean, helping the system remain stable when there are noisy values:

```python
# Get the median value from the N most recent frames
def get_median_ear(self):
    if len(self.ear_history) > 0:
        return np.median(self.ear_history)
    return 0
```

## 3. Kalman Filter

Formula for the one-dimensional Kalman filter used to smooth EAR data:

```
Prediction:
x̂_k|k-1 = A × x̂_k-1|k-1
P_k|k-1 = A × P_k-1|k-1 × A^T + Q

Update:
K_k = P_k|k-1 × H^T × (H × P_k|k-1 × H^T + R)^-1
x̂_k|k = x̂_k|k-1 + K_k × (z_k - H × x̂_k|k-1)
P_k|k = (I - K_k × H) × P_k|k-1
```

Where:
- `x̂_k|k-1` is the state estimate before observation
- `x̂_k|k` is the state estimate after observation
- `z_k` is the measurement value (EAR)
- `P_k|k-1` and `P_k|k` are the error covariance matrices of the estimate
- `K_k` is the Kalman gain
- `A` is the state transition matrix (typically 1 for simple cases)
- `H` is the observation matrix (typically 1 for simple cases)
- `Q` is the process noise covariance
- `R` is the measurement noise covariance

The system uses the Kalman filter to remove noise from EAR values, helping to detect drowsiness more accurately, especially in challenging lighting conditions.

## 4. Hysteresis Technique

This technique helps avoid rapid oscillation between states when the measured value fluctuates around the detection threshold:

```python
# Apply hysteresis to avoid state oscillation
if current_state == "NORMAL":
    # Require value to be significantly below threshold to transition to warning state
    threshold_to_warning = self.EAR_THRESHOLD - 0.02
    
    if ear < threshold_to_warning and consecutive_frames > self.WARNING_THRESHOLD:
        new_state = "WARNING"
elif current_state == "WARNING":
    # Require value to be significantly above threshold to return to normal state
    threshold_to_normal = self.EAR_THRESHOLD + 0.02
    
    if ear > threshold_to_normal:
        recovery_frames += 1
        if recovery_frames > self.RECOVERY_THRESHOLD:
            new_state = "NORMAL"
            recovery_frames = 0
    # Require value to be significantly below threshold to transition to alert state
    threshold_to_alert = self.EAR_THRESHOLD - 0.05
    
    if ear < threshold_to_alert and consecutive_frames > self.ALERT_THRESHOLD:
        new_state = "ALERT"
```

## 5. Windowed Statistics Method

This method analyzes different statistics within a data window, not just the average value:

```
EAR_variability = σ_EAR / μ_EAR
```

Where:
- `σ_EAR` is the standard deviation of EAR values in the window
- `μ_EAR` is the average value of EAR in the window

This variability is used to detect eye blink patterns (quick eye opening and closing) versus drowsiness patterns (eyes gradually closing and staying closed for extended periods).

```python
# Calculate variability in window
def calculate_ear_variability(self):
    if len(self.ear_history) > 5:  # Need at least 5 samples
        std_dev = np.std(self.ear_history)
        mean_val = np.mean(self.ear_history)
        if mean_val > 0:
            return std_dev / mean_val
    return 0
```

## 6. Multi-Sensor Data Fusion

Formula for combining data from multiple sources (EAR, head position, hand position):

```
drowsiness_score = w₁ × normalized_EAR + w₂ × normalized_head_pose + w₃ × normalized_blink_rate
distraction_score = w₄ × normalized_head_pose + w₅ × normalized_hand_position
```

Where:
- `w₁` to `w₅` are weights calibrated based on experimentation
- Normalized values are in the range [0, 1]

This composite score provides a more robust indication of drowsiness or distraction state, minimizing the impact of noise from individual sensors.
