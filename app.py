from flask import Flask, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from transformers import pipeline
from PIL import Image
import io
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash,check_password_hash
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DB_CONFIG = {
    'host': 'localhost',
    'database': 'dish_to_recipe',
    'user': 'postgres',
    'password': 'papadam'
}

def get_db_connection():
    """Create and return a new database connection"""
    return psycopg2.connect(**DB_CONFIG)


# Configure Gemini API
API_KEY = "AIzaSyC7fG0q-3G1OLp5gyBfn2LF3VnDtPKPlfY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Load Hugging Face image classification model
classifier = pipeline("image-classification", model="Shresthadev403/food-image-classification")

# Load Gemini AI model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_recipe(dish_name):
    """Generates a recipe for the classified dish using Gemini AI."""
    prompt = f"Generate a detailed recipe for {dish_name}. Include brief ingredients, step-by-step brief instructions, and cooking time, each instructions should be displayed on a new line as bullet points.All this should be done briefly"
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
    
@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return jsonify({"error": "Invalid email address"}), 400

    try:
        conn = get_db_connection()  # ✅ Using the DB_CONFIG helper
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if email exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 400

        # Insert new user
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id",
            (email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/signin', methods=['POST'])
def login():
    try:
        # Get JSON data from request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Create new connection
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if user exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            return jsonify({
                "message": "Login successful",
                "email": user['email']
            })
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        # Always close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        email = data.get('email')
        message = data.get('message')

        if not all([email, message]):
            return jsonify({"error": "Email and message are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user_id from email
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]

        # Insert feedback with user_id
        cursor.execute(
            "INSERT INTO feedback (user_id, message) VALUES (%s, %s) RETURNING id, submission_time",
            (user_id, message)
        )
        feedback_data = cursor.fetchone()
        conn.commit()

        return jsonify({
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_data[0],
            "submission_time": feedback_data[1].isoformat()
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/feedback', methods=['GET'])
def get_all_feedback():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('''
            SELECT u.email, f.message, f.submission_time
            FROM feedback f
            JOIN users u ON f.user_id = u.id
            ORDER BY f.submission_time DESC
        ''')
        feedback_list = cursor.fetchall()

        return jsonify([dict(row) for row in feedback_list]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)
