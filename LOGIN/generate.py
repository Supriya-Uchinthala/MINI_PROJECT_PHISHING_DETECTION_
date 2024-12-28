import os
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Directories where the QR codes are stored
spam_dir = 'qrcodes/spam'
ham_dir = 'qrcodes/ham'

# Function to convert QR code image to a flat feature vector (pixel values)
def image_to_features(image_path, image_size=(64, 64)):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize(image_size)  # Resize to uniform size
    img_array = np.array(img)  # Convert to numpy array
    return img_array.flatten()  # Flatten into 1D array

# Initialize lists to store features (X) and labels (y)
X = []
y = []

# Load all images from the 'spam' and 'ham' directories
for label, directory in zip(['spam', 'ham'], [spam_dir, ham_dir]):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):  # Only process PNG files
            image_path = os.path.join(directory, filename)
            features = image_to_features(image_path)
            X.append(features)
            y.append(label)

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Encode labels (spam = 1, ham = 0)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train the Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Save the trained model
joblib.dump(rf_classifier, 'random_forest_model.pkl')
print("Model saved as 'random_forest_model.pkl'")

# Save the label encoder (to use for predictions)
joblib.dump(label_encoder, 'label_encoder.pkl')
print("Label encoder saved as 'label_encoder.pkl'")
