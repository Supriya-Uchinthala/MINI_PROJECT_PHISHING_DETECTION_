from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import validators
import joblib

app = Flask(__name__)

# Load the trained Random Forest model and the label encoder
rf_classifier = joblib.load('D:\\MINI-PROJECT\\QR-CODE\\random_forest_model.pkl')
label_encoder = joblib.load('D:\\MINI-PROJECT\\QR-CODE\\label_encoder.pkl')

def image_to_features(npimg):
    """
    Convert the uploaded QR code image to features for prediction.
    """
    # Convert the uploaded image (as npimg) into a grayscale image and resize it
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64))  # Resize to match model's training input dimensions
    
    if img is None:
        raise ValueError("Could not read the image properly.")
    
    # Flatten the image to match the expected feature size (4096 features)
    features = img.flatten()

    return features

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        # Convert the file to a numpy array
        npimg = np.frombuffer(file.read(), np.uint8)
        # Convert the numpy array to an image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Create a QR Code detector
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            response = {
                'status': 'success',
                'data': data,
                'type': 'unknown'
            }

            # If the QR code contains a URL, classify it using the Random Forest model
            if validators.url(data):
                # Preprocess the QR code URL and classify it
                prediction = rf_classifier.predict([image_to_features(npimg)])
                result = label_encoder.inverse_transform(prediction)
                
                # Use the model prediction to classify as spam or ham
                response['type'] = 'spam' if result[0] == 'spam' else 'ham'
            else:
                # If it's not a URL, assume it's safe or do further processing as needed
                response['type'] = 'ham'

        else:
            response = {
                'status': 'fail',
                'message': 'No QR Code found'
            }

        return jsonify(response)
    else:
        return jsonify({'status': 'fail', 'message': 'No file uploaded'})

if __name__ == '__main__':
    app.run(port=5003)
