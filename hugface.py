from transformers import pipeline

classifier = pipeline("image-classification", model="Shresthadev403/food-image-classification")

from PIL import Image

# Load image (replace 'food.jpg' with your image file path)
image = Image.open("food.jpg")

results = classifier(image)

# Print the results
for result in results:
    print(f"Label: {result['label']}, Confidence: {result['score']:.4f}")

from transformers import AutoModelForImageClassification, AutoProcessor
import torch

model_name = "Shresthadev403/food-image-classification"
model = AutoModelForImageClassification.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)

inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# Convert logits to probabilities
probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

# Get the predicted class
predicted_label = probabilities.argmax().item()

# Print the result
print(f"Predicted class: {model.config.id2label[predicted_label]}")