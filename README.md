# OCR-IC-Reader

## Description

<p>This project is a fork of https://github.com/TechMi97/Malaysian-IC-OCR. It aims to extract text from identity card (IC) images using Optical Character Recognition (OCR) techniques. The primary goal is to enhance and improve the original functionality.</p>

## Features

<ul>
<li>Text extraction from IC images</li>
<li>Image preprocessing for improved OCR accuracy</li>
<li>User-friendly web interface (powered by Flask)</li>
<li>Option to use either Tesseract or EasyOCR for text recognition</li>
</ul>

## Installation

**Prerequisites:**

* Python 3.8+
* Conda (for environment management)
* Tesseract OCR (install separately, e.g., using Homebrew: `brew install tesseract`)

**Steps:**

1. Clone the repository:
   ```bash
   git clone https://github.com/faridhmad/malaysian-ic-ocr-enhanced.git
   ```

      ```bash
   cd malaysian-ic-ocr-enhanced
   ```

2. Create a Conda environment:
   ```bash
   conda create -n my_ocr_env python=3.8
   ```

3. Activate the environment:
   ```bash
   conda activate my_ocr_env
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. **Update the Tesseract Path (For Mac):**

   If you installed Tesseract using Homebrew, first run the following command in your terminal to find the correct path:

   ```bash
   which tesseract
   ```

   Then, update your Python code (`app.py` and `app2.py`) with the path you found:

   ```
   pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Replace with your actual path
   ```

6. **Run the application:**
   ```bash
   export FLASK_APP=app
   flask run
   ```

## Usage

This project contains two Flask applications for extracting text from IC images:

* **`app.py`:** Uses the Tesseract OCR engine. To run:
   ```bash
   export FLASK_APP=app
   flask run
   ```

* **`app2.py`:** Uses the EasyOCR engine. To run:
   ```bash
   export FLASK_APP=app2
   flask run
   ```

1.  **Open a web browser and navigate to `http://127.0.0.1:5000/`.** (for either app)
2.  **Upload an image of an IC.**
3.  **The extracted text will be displayed on the screen along with the OCR engine used.**

