import google.generativeai as genai

def get_recipe(dish_name, api_key):
    """Generates a recipe for the given dish name using Google's Gemini API."""
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Give me a detailed recipe for {dish_name}, including ingredients and step-by-step instructions."
    response = model.generate_content(prompt)
    
    return response.text if response.text else "No recipe found."

if __name__ == "__main__":
    API_KEY = "AIzaSyC5eyRZmUJrmd5IOSyDKZNgHRvuDGSka-c"  # Replace with your actual API key
    dish = input("Enter the dish name: ")
    recipe = get_recipe(dish, API_KEY)
    print("\nGenerated Recipe:\n")
    print(recipe)
