#Dish to Recipe 🍴
Dish to Recipe is a web application that allows users to upload an image of a dish, detect the dish name using a Hugging Face AI model, and generate a recipe using the Gemini API. The project combines image classification, recipe generation, and a user-friendly frontend to create a seamless experience.

#Features ✨
Image Upload: Users can upload an image of a dish.

Dish Detection: The Hugging Face AI model identifies the dish in the image.

Recipe Generation: The Gemini API generates a recipe based on the detected dish.

Responsive Design: The frontend is designed to work on all screen sizes.

Parallax Effect: A visually appealing parallax background enhances the user experience.

Typing Animation: A welcoming typing animation greets users.

#Technologies Used 🛠️
Frontend: HTML, CSS, JavaScript

Backend: Flask (Python)

AI Model: Hugging Face (Shresthadev403/food-image-classification)

Recipe API: Gemini API

Fonts: Google Fonts (Poppins, Roboto, Playfair Display)

Setup Instructions 🚀
Prerequisites
Python 3.x

Flask (pip install flask)

Hugging Face Transformers (pip install transformers)

Requests (pip install requests)

Steps
Clone the Repository:

bash
Copy
git clone https://github.com/your-username/dish-to-recipe.git
cd dish-to-recipe
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Run the Backend:

bash
Copy
python app.py
The backend will start at http://localhost:5000.

Open the Frontend:

Open the index.html file in your browser.

Alternatively, use a local server (e.g., python -m http.server).

Upload an Image:

Upload an image of a dish.

The app will detect the dish and display the recipe.
