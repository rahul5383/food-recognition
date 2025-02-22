from flask import Flask, request, jsonify
from transformers import pipeline
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Load Hugging Face model
classifier = pipeline("image-classification", model="Shresthadev403/food-image-classification")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Read the uploaded image
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))

    # Classify the image using Hugging Face model
    results = classifier(image)

    # Extract the top result
    top_result = results[0]
    dish_name = top_result['label']
    confidence = top_result['score']

    # Return the dish name and confidence
    return jsonify({
        "dish": dish_name,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(debug=True)