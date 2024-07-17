import os
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import easyocr
import cv2
import numpy as np

# Define a folder to store uploaded images (not in static)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # Secure filename and save the original image
            filename = secure_filename(file.filename)
            original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the uploaded image to the designated folder before opening it
            file.save(original_image_path)  
            image = Image.open(original_image_path).convert('RGB')

            # Enhanced Image Preprocessing with OpenCV
            opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)

            # Convert back to PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))

            # OCR with EasyOCR (using the preprocessed image)
            reader = easyocr.Reader(['en'], gpu=True)

            # Pass the file path to EasyOCR, not the image object
            bounds = reader.readtext(original_image_path, detail=0, paragraph=True, x_ths=0.7)

            new_text = ' '.join(bounds)

            # Draw bounding boxes
            draw = ImageDraw.Draw(pil_image)
            for bound in reader.readtext(original_image_path, detail=1):
                p0, p1, p2, p3 = bound[0]
                draw.line([*p0, *p1, *p2, *p3, *p0], fill="yellow", width=2)
            
            # Save processed image with bounding boxes
            processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "processed_" + filename)
            pil_image.save(processed_image_path)

            # Render template with extracted text and image URLs
            return render_template(
                'upload.html',
                msg='IC Successfully processed',
                extracted_text=new_text,
                img_src=url_for('uploaded_file', filename='processed_' + filename),
                original_filename=url_for('uploaded_file', filename=filename),
                ocr_engine='EasyOCR',
            )
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
