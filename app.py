from flask import Flask, request, jsonify
from transformers import pipeline
from PIL import Image
import io
from flask_cors import CORS
import google.generativeai as genai  # Import Gemini API

# Set up Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
API_KEY = "AIzaSyC7fG0q-3G1OLp5gyBfn2LF3VnDtPKPlfY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Load Hugging Face image classification model
classifier = pipeline("image-classification", model="Shresthadev403/food-image-classification")

# Load Gemini AI model
model = genai.GenerativeModel("gemini-pro")

def generate_recipe(dish_name):
    """Generates a recipe for the classified dish using Gemini AI."""
    prompt = f"Generate a detailed recipe for {dish_name}. Include ingredients, step-by-step brief instructions, and cooking time, each instructions should be displayed on a new line as bullet points."
    
    try:
        response = model.generate_content(prompt)
        return response.text  # Extract generated text
    except Exception as e:
        return f"Error: {str(e)}"

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

    # Generate recipe using Gemini AI
    recipe = generate_recipe(dish_name)

    # Return the dish name, confidence, and recipe
    return jsonify({
        "dish": dish_name,
        "recipe": recipe
    })

if __name__ == '__main__':
    app.run(debug=True)
