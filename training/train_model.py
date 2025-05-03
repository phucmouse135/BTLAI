import os
import cv2
import numpy as np
import tensorflow as tf
# Update imports for newer TensorFlow versions
try:
    from tensorflow.keras.utils import to_categorical
except ImportError:
    # For newer versions where keras is a separate package
    from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.detection_model import SafetyMonitoringModel

class ModelTrainer:
    def __init__(self, data_dir, model_save_path):
        """
        Initialize the model trainer
        
        Args:
            data_dir: Directory containing training data
            model_save_path: Path to save the trained model
        """
        self.data_dir = data_dir
        self.model_save_path = model_save_path
        self.model = SafetyMonitoringModel()
        
    def load_and_preprocess_data(self, img_size=(100, 100), test_split=0.2):
        """
        Load and preprocess images for training
        
        Args:
            img_size: Size to resize images to
            test_split: Fraction of data to use for testing
            
        Returns:
            Tuple of (train_data, train_labels, test_data, test_labels)
        """
        # Define class folders
        classes = ['focused', 'distracted']
        
        images = []
        labels = []
        
        # Load images from each class
        for class_idx, class_name in enumerate(classes):
            class_path = os.path.join(self.data_dir, class_name)
            
            if not os.path.exists(class_path):
                print(f"Warning: Class path {class_path} does not exist")
                continue
                
            print(f"Loading {class_name} images...")
            
            # Get all image files
            for img_file in tqdm(os.listdir(class_path)):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(class_path, img_file)
                    
                    # Load and preprocess image
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"Warning: Could not read {img_path}")
                        continue
                        
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, img_size)
                    img = img / 255.0  # Normalize
                    
                    images.append(img)
                    labels.append(class_idx)
        
        if not images:
            raise ValueError("No valid images found in the data directory")
            
        # Convert to numpy arrays
        X = np.array(images)
        y = np.array(labels)
        
        # Convert labels to one-hot encoding
        y = to_categorical(y, num_classes=len(classes))
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_split, random_state=42, stratify=y
        )
        
        print(f"Training data shape: {X_train.shape}, Labels shape: {y_train.shape}")
        print(f"Testing data shape: {X_test.shape}, Labels shape: {y_test.shape}")
        
        return X_train, y_train, X_test, y_test
    
    def train(self, epochs=20, batch_size=32, augment=True):
        """
        Train the model
        
        Args:
            epochs: Number of training epochs
            batch_size: Batch size for training
            augment: Whether to use data augmentation
            
        Returns:
            Training history
        """
        # Load and preprocess data
        X_train, y_train, X_test, y_test = self.load_and_preprocess_data()
        
        # Data augmentation (if enabled)
        if augment:
            data_augmentation = tf.keras.Sequential([
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomRotation(0.1),
                tf.keras.layers.RandomZoom(0.1),
                tf.keras.layers.RandomBrightness(0.1),
                tf.keras.layers.RandomContrast(0.1),
            ])
            
            # Create augmented dataset
            train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
            train_dataset = train_dataset.shuffle(buffer_size=1024)
            train_dataset = train_dataset.batch(batch_size)
            train_dataset = train_dataset.map(
                lambda x, y: (data_augmentation(x, training=True), y),
                num_parallel_calls=tf.data.AUTOTUNE
            )
            train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
            
            # Train with dataset
            history = self.model.model.fit(
                train_dataset,
                validation_data=(X_test, y_test),
                epochs=epochs
            )
        else:
            # Train without augmentation
            history = self.model.train(
                X_train, y_train,
                validation_data=X_test,
                validation_labels=y_test,
                epochs=epochs,
                batch_size=batch_size
            )
        
        # Save the trained model
        self.model.save_model(self.model_save_path)
        print(f"Model saved to {self.model_save_path}")
        
        # Evaluate on test data
        evaluation = self.model.model.evaluate(X_test, y_test)
        print(f"Test accuracy: {evaluation[1]:.4f}")
        
        return history
    
    def plot_training_history(self, history):
        """
        Plot training history metrics
        
        Args:
            history: Training history returned by model.fit()
        """
        # Create figure
        plt.figure(figsize=(12, 4))
        
        # Plot accuracy
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='lower right')
        
        # Plot loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper right')
        
        plt.tight_layout()
        
        # Save plot
        plots_dir = os.path.join(os.path.dirname(self.model_save_path), 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        plt.savefig(os.path.join(plots_dir, 'training_history.png'))
        plt.close()
        
if __name__ == "__main__":
    # Example usage
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    model_save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'saved_model')
    
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    trainer = ModelTrainer(data_dir, model_save_path)
    history = trainer.train()
    trainer.plot_training_history(history)