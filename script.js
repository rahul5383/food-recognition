// Typing Animation
const typedText = document.getElementById('typed-text');
const text = "Welcome to Dish to Recipe!";
let index = 0;

function type() {
  if (index < text.length) {
    typedText.textContent += text.charAt(index);
    index++;
    setTimeout(type, 100); // Adjust typing speed here
  } else {
    // Stop the cursor from blinking after typing is done
    document.querySelector('.cursor').style.animation = 'none';
  }
}

// Start the typing animation
type();

// Parallax Effect
window.addEventListener('scroll', () => {
  const parallax = document.querySelector('.parallax');
  let scrollPosition = window.pageYOffset;

  // Adjust the background position based on scroll
  parallax.style.transform = `translateY(${scrollPosition * 0.5}px)`;
});

// Handle Image Upload and Recipe Generation
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = document.getElementById('dishImage').files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  // Show loading spinner
  document.getElementById('loading').style.display = 'block';
  document.getElementById('result').innerText = '';

  try {
    // Send image to backend
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Backend response:", data);  // Log the response

    // Format the recipe output
    const recipeOutput = `
      <div class="recipe-output">
        <h2>🍽️ Dish: ${data.dish}</h2>
        <h3>📝 Recipe:</h3>
        ${formatRecipe(data.recipe)}
      </div>
    `;

    // Display result
    document.getElementById('result').innerHTML = recipeOutput;
  } catch (error) {
    console.error("Error:", error);  // Log the error
    document.getElementById('result').innerText = '❌ Error detecting dish or fetching recipe. Please try again.';
  } finally {
    // Hide loading spinner
    document.getElementById('loading').style.display = 'none';
  }
});

// Function to format the recipe
function formatRecipe(recipe) {
  // Split the recipe into ingredients and instructions
  const [ingredientsPart, instructionsPart] = recipe.split('**Instructions:**');

  // Format ingredients
  const ingredients = ingredientsPart
    .replace('**Ingredients:**', '') // Remove the "Ingredients" heading
    .split('-') // Split into individual ingredients
    .filter(item => item.trim() !== '') // Remove empty items
    .map(item => `<li>${item.trim()}</li>`); // Wrap each ingredient in <li>

  // Format instructions
  const instructions = instructionsPart
    .split('-') // Split into individual steps
    .filter(item => item.trim() !== '') // Remove empty items
    .map((item, index) => `<li>${item.trim()}</li>`); // Wrap each step in <li>

  // Return structured HTML
  return `
    <h3>Ingredients:</h3>
    <ul>${ingredients.join('')}</ul>
    <h3>Instructions:</h3>
    <ol>${instructions.join('')}</ol>
  `;
}
