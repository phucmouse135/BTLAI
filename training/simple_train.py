import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SimpleModelTrainer:
    def __init__(self, data_dir, model_save_path):
        """
        Initialize the model trainer using scikit-learn instead of TensorFlow
        
        Args:
            data_dir: Directory containing training data
            model_save_path: Path to save the trained model
        """
        self.data_dir = data_dir
        self.model_save_path = model_save_path
        self.model = SVC(probability=True)
        self.scaler = StandardScaler()
        
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
            
            # Get all image files (only jpg, not json)
            image_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for img_file in tqdm(image_files):
                img_path = os.path.join(class_path, img_file)
                
                # Load and preprocess image
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Warning: Could not read {img_path}")
                    continue
                    
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, img_size)
                
                # Extract simple features instead of using raw pixels
                # Convert to grayscale for HOG features
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                
                # Calculate Histogram of Oriented Gradients
                # (simplified approach)
                features = []
                
                # Add average pixel values in different regions as features
                cell_size = 20
                for i in range(0, img_size[0], cell_size):
                    for j in range(0, img_size[1], cell_size):
                        cell = gray[i:i+cell_size, j:j+cell_size]
                        if cell.size > 0:
                            features.append(np.mean(cell))
                
                # Add color histogram features
                for channel in range(3):
                    hist = cv2.calcHist([img], [channel], None, [32], [0, 256])
                    features.extend(hist.flatten())
                
                images.append(features)
                labels.append(class_idx)
        
        if not images:
            raise ValueError("No valid images found in the data directory")
            
        # Convert to numpy arrays
        X = np.array(images)
        y = np.array(labels)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_split, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        print(f"Training data shape: {X_train.shape}, Labels shape: {y_train.shape}")
        print(f"Testing data shape: {X_test.shape}, Labels shape: {y_test.shape}")
        
        return X_train, y_train, X_test, y_test
    
    def train(self):
        """
        Train the model
            
        Returns:
            Training accuracy and test accuracy
        """
        # Load and preprocess data
        X_train, y_train, X_test, y_test = self.load_and_preprocess_data()
        
        # Train the model
        print("Training SVM model...")
        self.model.fit(X_train, y_train)
        
        # Calculate accuracies
        train_accuracy = self.model.score(X_train, y_train)
        test_accuracy = self.model.score(X_test, y_test)
        
        print(f"Training accuracy: {train_accuracy:.4f}")
        print(f"Test accuracy: {test_accuracy:.4f}")
        
        # Save the trained model
        os.makedirs(os.path.dirname(self.model_save_path), exist_ok=True)
        with open(self.model_save_path, 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        print(f"Model saved to {self.model_save_path}")
        
        return train_accuracy, test_accuracy
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """
        Plot confusion matrix
        """
        from sklearn.metrics import confusion_matrix
        import seaborn as sns
        
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['Focused', 'Distracted'],
                   yticklabels=['Focused', 'Distracted'])
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        
        # Save plot
        plots_dir = os.path.join(os.path.dirname(self.model_save_path), 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        plt.savefig(os.path.join(plots_dir, 'confusion_matrix.png'))
        plt.close()

# Function to run from main.py
def train_model():
    """Simplified training function that doesn't rely on TensorFlow"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    model_save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  'models', 'saved_model.pkl')
    
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    trainer = SimpleModelTrainer(data_dir, model_save_path)
    train_acc, test_acc = trainer.train()
    
    # Test prediction and plot confusion matrix if test data exists
    X_train, y_train, X_test, y_test = trainer.load_and_preprocess_data()
    if len(X_test) > 0:
        y_pred = trainer.model.predict(X_test)
        trainer.plot_confusion_matrix(y_test, y_pred)
    
    return train_acc, test_acc

if __name__ == "__main__":
    train_model()