from flask import Flask, request, jsonify, send_file, render_template_string
import numpy as np
import cv2
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Flask server is running!", 200

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    
    # Convert the image file to a numpy array
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Failed to decode image"}), 400

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract coordinates of bounding boxes around detected contours
    plant_coordinates = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2
        plant_coordinates.append({"x": center_x, "y": center_y})

        # Draw a bounding box and label on the image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, f'Plant {i+1}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Convert the image to a format suitable for sending via Flask
    _, img_encoded = cv2.imencode('.jpg', img)
    img_bytes = img_encoded.tobytes()

    # Create a BytesIO object to serve the image
    img_io = BytesIO(img_bytes)
    img_io.seek(0)

    # Generate HTML with the image
    html_content = f'''
    <html>
    <body>
        <h1>Detected Plants</h1>
        <img src="data:image/jpeg;base64,{base64.b64encode(img_bytes).decode('utf-8')}" alt="Processed Image">
        <p>Coordinates: {plant_coordinates}</p>
    </body>
    </html>
    '''

    # Send coordinates back to the Arduino (for demonstration, this example assumes the request body is JSON)
    response = {
        "coordinates": plant_coordinates,
        "message": "Plants detected and annotated"
    }

    return render_template_string(html_content), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
