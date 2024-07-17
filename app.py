import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import cv2

# Configure Tesseract command path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Define a folder to store and later serve the images
root_dir = "static" # This is the folder where the app.py file is located
UPLOAD_FOLDER = os.path.join(root_dir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Initialize Flask application
app = Flask(__name__)

# Function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# Route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # Check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        
        file = request.files['file']
        # If no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')
        
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            original_image_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save the uploaded image to the designated folder before opening it
            file.save(original_image_path)
            image = cv2.imread(original_image_path)

            # Convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Apply thresholding
            gray = cv2.threshold(gray, 200, 255, cv2.THRESH_TRUNC)[1]

            # Save the processed image
            processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_" + filename)
            cv2.imwrite(processed_image_path, gray)

            # Extract text from the processed image using Tesseract
            extracted_text = pytesseract.image_to_string(Image.open(processed_image_path), 
                                                        config='--psm 3')  # Try different PSM values
            # Render template with extracted text and image URLs
            return render_template(
                'upload.html',
                msg='IC Successfully processed',
                extracted_text=extracted_text,
                img_src=url_for('static', filename='uploads/processed_' + filename),
                original_filename=url_for('static', filename='uploads/' + filename),
                ocr_engine='Tesseract'
            )
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
