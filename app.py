from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)

# Global variable to store the latest coordinates
latest_coordinates = {"x": None, "y": None}

def detect_largest_tree(frame):
    """
    Detect the largest tree in the given frame.
    Draw a bounding box around the largest tree and return its coordinates.
    """
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None

        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw the bounding box and label on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, 'Largest Tree', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return {"x": center_x, "y": center_y}
    except Exception as e:
        print(f"Error in detect_largest_tree: {e}")
        return None

@app.route('/')
def home():
    return 'Welcome to the Flask Server!'

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Endpoint to receive video frames from the ESP32-CAM and process them.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    try:
        image_file = request.files['image']
        image_bytes = image_file.read()
        image_array = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Failed to decode image"}), 400

        global latest_coordinates
        coordinates = detect_largest_tree(frame)
        if coordinates:
            latest_coordinates = coordinates
        else:
            return jsonify({"error": "No trees detected"}), 404

        # Encode the processed image to display on the server
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Display image and coordinates on the server page
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Processed Image</title>
        </head>
        <body>
            <h1>Processed Image with Coordinates</h1>
            <img src="data:image/jpeg;base64,{img_base64}" alt="Processed Image"/>
            <p>Coordinates: X={latest_coordinates["x"]}, Y={latest_coordinates["y"]}</p>
        </body>
        </html>
        '''

        return html_content
    except Exception as e:
        print(f"Error in upload_image: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    """
    Endpoint to get the latest coordinates of the detected largest tree.
    """
    try:
        return jsonify(latest_coordinates)
    except Exception as e:
        print(f"Error in get_coordinates: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
