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
  
  // Check login status first
  if (!isLoggedIn()) {
    showLoginPrompt();
    return;
  }

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

    console.log("Full recipe text:", data.recipe);

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
  const ingredientsSplit = recipe.split(/\*\*Ingredients:\*\*/i);
  const instructionsSplit = recipe.split(/\*\*Instructions:\*\*/i);

  const ingredientsPart = ingredientsSplit[1] || '';
  const instructionsPart = instructionsSplit[1] || '';

  const ingredients = ingredientsPart
    .split('*') // Markdown uses `*` or `-` for lists
    .filter(item => item.trim())
    .map(item => `<li>${item.trim()}</li>`);

  const instructions = instructionsPart
    .split('*')
    .filter(item => item.trim())
    .map(item => `<li>${item.trim()}</li>`);

  return `
    <h3>Ingredients:</h3>
    <ul>${ingredients.join('')}</ul>
    <h3>Instructions:</h3>
    <ul>${instructions.join('')}</ul>
  `;
}

// Authentication functions
function isLoggedIn() {
  return localStorage.getItem('isLoggedIn') === 'true';
}

function showLoginPrompt() {
  const prompt = document.getElementById('loginPrompt');
  prompt.style.display = 'flex';
  setTimeout(() => prompt.classList.add('show'), 10);
}

function hideLoginPrompt() {
  const prompt = document.getElementById('loginPrompt');
  prompt.classList.remove('show');
  setTimeout(() => prompt.style.display = 'none', 300);
}

// Check login status and update UI
function updateAuthUI() {
  const loggedIn = isLoggedIn();
  const userEmail = localStorage.getItem('email');
  
  if (loggedIn) {
    // User is logged in
    document.getElementById('signUpBtn').style.display = 'none';
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'inline-block';
    document.getElementById('usernameDisplay').textContent = `Welcome, ${userEmail}!`;
    document.getElementById('uploadForm').style.opacity = '1';
    document.getElementById('uploadForm').style.pointerEvents = 'auto';
    hideLoginPrompt();
  } else {
    // User is logged out
    document.getElementById('signUpBtn').style.display = 'inline-block';
    document.getElementById('loginBtn').style.display = 'inline-block';
    document.getElementById('logoutBtn').style.display = 'none';
    document.getElementById('usernameDisplay').textContent = '';
    document.getElementById('uploadForm').style.opacity = '0.5';
    document.getElementById('uploadForm').style.pointerEvents = 'none';
  }
}

function handleLogout() {
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('email');
  updateAuthUI();
  window.location.href = 'signin.html';
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  updateAuthUI();
  
  // Add event listener to logout button
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
  
  // Show prompt if not logged in when page loads
  if (!isLoggedIn()) {
    showLoginPrompt();
  }
});

// Feedback Form Functionality
document.addEventListener('DOMContentLoaded', function() {
  // Show feedback button after page loads
  setTimeout(() => {
    document.getElementById('feedbackContainer').classList.add('visible');
  }, 3000);

  // Toggle feedback form visibility
  document.getElementById('feedbackBtn').addEventListener('click', function() {
    const form = document.getElementById('feedbackForm');
    form.style.display = form.style.display === 'block' ? 'none' : 'block';
  });

  function showFeedbackMessage(text, isSuccess) {
    const messageDiv = document.querySelector('.feedback-message');
    messageDiv.textContent = text;
    messageDiv.style.color = isSuccess ? '#4CAF50' : '#e74c3c';
    
    setTimeout(() => {
      messageDiv.textContent = '';
    }, 3000);
  }
});

document.getElementById('submitFeedback').addEventListener('click', async function() {
    const message = document.getElementById('feedbackMessage').value.trim();
    const userEmail = localStorage.getItem('email');
    
    if (!userEmail) {
        showFeedbackMessage('Please log in to submit feedback', false);
        return;
    }

    if (!message) {
        showFeedbackMessage('Please enter your feedback', false);
        return;
    }

    // Disable button during submission
    this.disabled = true;
    this.textContent = 'Submitting...';

    try {
        const response = await fetch('http://localhost:5000/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email: userEmail,  // Server will look up ID
                message 
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit feedback');
        }

        document.getElementById('feedbackMessage').value = '';
        showFeedbackMessage('Thank you for your feedback!', true);
        
        setTimeout(() => {
            document.getElementById('feedbackForm').style.display = 'none';
        }, 2000);
    } catch (error) {
        showFeedbackMessage(error.message, false);
    } finally {
        this.disabled = false;
        this.textContent = 'Submit';
    }
});
