from flask import Flask, request, jsonify
from transformers import pipeline
from PIL import Image
import io
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
API_KEY = "AIzaSyC7fG0q-3G1OLp5gyBfnVnDtPKPlfY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Load Hugging Face image classification model
classifier = pipeline("image-classification", model="Shresthadev403/food-image-classification")

# Load Gemini AI model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_recipe(dish_name):
    """Generates a recipe for the classified dish using Gemini AI."""
    prompt = f"Generate a detailed recipe for {dish_name}. Include ingredients, step-by-step brief instructions, and cooking time, each instructions should be displayed on a new line as bullet points."
    print("Prompt sent to Gemini:", prompt)  # Log the prompt

    try:
        response = model.generate_content(prompt)
        print("Gemini response:", response.text)  # Log the response
        return response.text
    except Exception as e:
        print("Error generating recipe:", str(e))  # Log the error
        return f"Error: {str(e)}"

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        print("File received:", file.filename)  # Log the filename
        image = Image.open(io.BytesIO(file.read()))
        print("Image opened successfully")  # Log success

        results = classifier(image)
        print("Classification results:", results)  # Log the results
        top_result = results[0]
        dish_name = top_result['label']

        recipe = generate_recipe(dish_name)

        return jsonify({
            "dish": dish_name,
            "recipe": recipe
        })
    except Exception as e:
        print("Error in /upload route:", str(e))  # Log the error
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
