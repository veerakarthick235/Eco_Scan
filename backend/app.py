from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image
import numpy as np
import io

# ----------------- INITIALIZATION -----------------
# Initialize the Flask app
app = Flask(__name__)
# Enable CORS (Cross-Origin Resource Sharing) to allow the frontend to call this backend
CORS(app)

# Load the pre-trained MobileNetV2 model once when the server starts
# This model is trained on the ImageNet dataset and can recognize 1000 common objects
print("Loading TensorFlow model...")
model = MobileNetV2(weights='imagenet')
print("Model loaded successfully.")

# ----------------- DATABASES & MAPPINGS -----------------
# This dictionary holds our custom disposal information for different waste categories.
waste_database = {
    "bottle": { 
        "name": "Plastic Bottle", 
        "category": "Recycle ♻️", 
        "className": "recycle", 
        "instructions": "Empty the bottle, rinse it out, and put the cap back on before placing it in the recycling bin.", 
        "tip": "Recycling one plastic bottle can save enough energy to power a 60-watt bulb for 3 hours." 
    },
    "can": { 
        "name": "Aluminum Can", 
        "category": "Recycle ♻️", 
        "className": "recycle", 
        "instructions": "Rinse the can and place it in your recycling bin. Aluminum is infinitely recyclable!", 
        "tip": "Recycling aluminum saves 95% of the energy needed to make it from raw materials." 
    },
    "apple": { 
        "name": "Apple", 
        "category": "Compost 🌿", 
        "className": "compost", 
        "instructions": "Place this in your compost bin. It will decompose and enrich the soil.", 
        "tip": "Composting food scraps reduces methane emissions from landfills." 
    },
    "banana": { 
        "name": "Banana", 
        "category": "Compost 🌿", 
        "className": "compost", 
        "instructions": "Place this in your compost bin with other fruit and vegetable scraps.", 
        "tip": "Banana peels are rich in potassium and great for garden soil." 
    },
    "bag": { 
        "name": "Plastic Bag", 
        "category": "Trash 🗑️", 
        "className": "trash", 
        "instructions": "Most curbside programs do not accept plastic bags as they jam machinery. Dispose of them in the trash or find a special store drop-off.", 
        "tip": "Opt for reusable bags when shopping to reduce plastic waste." 
    },
    "cup": { 
        "name": "Paper Cup", 
        "category": "Check Locally ⚠️", 
        "className": "special", 
        "instructions": "Many paper cups have a plastic lining. Check your local program's rules. If in doubt, trash it.", 
        "tip": "Using a reusable coffee cup prevents hundreds of disposable cups from entering the waste stream each year." 
    }
}

# This crucial dictionary maps the AI model's technical labels to our simple database keys.
# You can expand this map to teach the app about new objects.
label_map = {
    'water_bottle': 'bottle',
    'soda_bottle': 'bottle',
    'pop_bottle': 'bottle',
    'beer_can': 'can',
    'apple': 'apple',
    'banana': 'banana',
    'plastic_bag': 'bag',
    'shopping_bag': 'bag',
    'coffee_mug': 'cup',
    'paper_towel': 'cup'
}

# ----------------- AI CLASSIFICATION LOGIC -----------------
def classify_with_ai(image_bytes):
    """
    Takes an image in bytes, preprocesses it, gets a prediction from the AI model,
    and maps the prediction to our waste database.
    """
    # MobileNetV2 expects images of size 224x224 pixels.
    # We open the image bytes, ensure it's in RGB format, and resize it.
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    
    # Convert the image to a NumPy array, which is a format TensorFlow understands.
    img_array = np.array(img)
    # Add an extra dimension because the model expects a "batch" of images.
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess the image array for MobileNetV2 (e.g., scaling pixel values).
    processed_img = preprocess_input(img_array)
    
    # Get the AI model's predictions.
    predictions = model.predict(processed_img)
    # Decode the predictions into human-readable labels and get the top 3 results.
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    
    # This print statement is essential for debugging and expanding the app's knowledge.
    # It shows you the AI's guesses in your terminal.
    print(f"AI Predictions: {decoded_predictions}")

    # Loop through the top predictions to see if any match our label_map.
    for _, label, confidence in decoded_predictions:
        if label in label_map:
            # If a match is found, get our custom category key.
            db_key = label_map[label]
            # Return the corresponding data from our waste database.
            return waste_database[db_key]
            
    # If none of the top predictions are in our label_map, return None.
    return None

# ----------------- API ENDPOINT -----------------
@app.route('/classify', methods=['POST'])
def classify_image_endpoint():
    """The main API endpoint that the frontend calls."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Read the image file into bytes.
        image_bytes = file.read()
        # Call our AI classification function.
        result = classify_with_ai(image_bytes)
        
        if result:
            # If the AI recognized the item, return the result as JSON.
            return jsonify(result)
        else:
            # If the item was not recognized, return the default "unidentified" response.
            unidentified_item = {
                "name": "Unidentified Item",
                "category": "Check Locally ⚠️",
                "className": "special",
                "instructions": "Our AI couldn't identify this item. Please check your local recycling and waste disposal guidelines.",
                "tip": "You can teach the AI by adding its predictions from the terminal into the 'label_map' in the code."
            }
            return jsonify(unidentified_item)

# ----------------- SCRIPT EXECUTION -----------------
if __name__ == '__main__':
    # This makes the script runnable with `python app.py`.
    # `debug=True` allows for automatic reloading when you save changes.
    app.run(debug=True, port=5000)