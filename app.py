from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Route to receive the image and process it
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Read the image file
    file = request.files['image']
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Failed to decode image"}), 400

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([35, 40, 40])  # Lower bound for green
    upper_green = np.array([85, 255, 255])  # Upper bound for green

    # Create a mask with the specified green range
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of the green areas in the image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    plant_coordinates = []
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Only consider large enough objects
            x, y, w, h = cv2.boundingRect(contour)
            plant_coordinates.append({"x": int(x + w / 2), "y": int(y + h / 2)})

    return jsonify({"coordinates": plant_coordinates}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
