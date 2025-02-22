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

    const data = await response.json();

    // Display result
    document.getElementById('result').innerHTML = `
      <h2>🍽️ Dish: ${data.dish}</h2>
      <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
      <p><strong>📝 Recipe:</strong> ${data.recipe}</p>
    `;
  } catch (error) {
    document.getElementById('result').innerText = '❌ Error detecting dish or fetching recipe. Please try again.';
  } finally {
    // Hide loading spinner
    document.getElementById('loading').style.display = 'none';
  }
});
