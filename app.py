import os
import numpy as np
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io

# --- Flask App Initialization ---
# We tell Flask where to find our web pages (in the 'static' folder)
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


# --- Load Keras Model ---
try:
    import tensorflow as tf
    from tensorflow import keras
    if os.path.exists('coconut_disease_model.h5'):
        model = keras.models.load_model('coconut_disease_model.h5')
        print("Model loaded successfully.")
    else:
        model = None
        print("Warning: 'coconut_disease_model.h5' not found.")

    class_names = [
        'Bud_Rot',
        'Bud_Root_Dropping',
        'Gray_Leaf_Spot',
        'Leaf_Rot',
        'Stem_Bleeding'
    ]
    print(f"Correct class names loaded: {class_names}")

except (ImportError, IOError) as e:
    print(f"Warning: TensorFlow/Keras could not be loaded. Error: {e}")
    model = None
    class_names = []


# --- Frontend Routes ---
# This route serves your main web page
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


# --- Helper Functions ---
def process_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = class_names[predicted_class_index].replace('_', ' ')
    confidence = float(np.max(predictions[0])) * 100
    return predicted_class_name, confidence


# --- Main API Endpoint ---
@app.route('/analyze', methods=['POST'])
def analyze():
    if model is None:
        return jsonify({'error': 'Model is not loaded on the server.'}), 500

    image_bytes = None
    if request.is_json:
        data = request.get_json()
        image_url = data.get('url')
        if not image_url: return jsonify({'error': 'No URL provided.'}), 400
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            image_bytes = response.content
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Failed to download image from URL: {e}'}), 400
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '': return jsonify({'error': 'No file selected.'}), 400
        image_bytes = file.read()
    else:
        return jsonify({'error': 'No file or URL provided.'}), 400

    try:
        prediction, confidence = process_image(image_bytes)
        return jsonify({'prediction': prediction, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': f'Error processing image: {e}'}), 500


# --- Main Execution ---
if __name__ == '__main__':
    print("\n--- To view the app, open your browser and go to: http://127.0.0.1:5000 ---\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
