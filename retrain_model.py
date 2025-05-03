import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import the training function
from training.simple_train import train_model

if __name__ == "__main__":
    print("Starting model retraining with enhanced face and eye detection...")
    # Run the training function
    train_acc, test_acc = train_model()
    print(f"Training completed with accuracy: {train_acc:.4f}")
    print(f"Test accuracy: {test_acc:.4f}")