from flask import Blueprint, request, jsonify
import os
from pdf2image import convert_from_path
import requests

process_file_controller = Blueprint('process_file_controller', __name__)

# Configuration variables for OCR API
ocr_api_url = "YOUR_OCR_API_URL"
api_key = "YOUR_API_KEY"

def process_pdf(file_path):
    """Process PDF by converting to images and sending to OCR API."""
    temp_folder = "temp_images"
    os.makedirs(temp_folder, exist_ok=True)
    combined_text = ""

    # Convert PDF to images
    images = convert_from_path(file_path)

    try:
        for idx, image in enumerate(images):
            image_path = os.path.join(temp_folder, f"page_{idx + 1}.png")
            image.save(image_path, "PNG")

            # Send the image to the OCR API
            with open(image_path, "rb") as img_file:
                response = requests.post(
                    ocr_api_url,
                    files={"file": img_file},
                    data={"api_key": api_key}
                )

            if response.status_code != 200:
                print(f"Error processing page {idx + 1}: {response.text}")
                continue

            # Extract and combine text
            text = response.json().get("text", "")
            combined_text += f"\nPage {idx + 1}:\n{text}"

    finally:
        # Cleanup temporary images
        for file in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, file))
        os.rmdir(temp_folder)

    return combined_text

def process_image(file_path):
    """Send an image file directly to the OCR API."""
    with open(file_path, "rb") as img_file:
        response = requests.post(
            ocr_api_url,
            files={"file": img_file},
            data={"api_key": api_key}
        )

    if response.status_code != 200:
        raise Exception(f"Error processing image: {response.text}")

    return response.json().get("text", "")

@process_file_controller.route('/process_file', methods=['POST'])
def process_file():
    file_path = request.form.get('file_path')  # File path is passed as a form parameter

    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    combined_text = ""

    try:
        if file_path.lower().endswith(".pdf"):
            combined_text = process_pdf(file_path)

        elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            combined_text = process_image(file_path)

        else:
            return jsonify({"error": "Unsupported file type. Only PDFs and images are allowed."}), 400

        # Write the extracted text into a target file
        target_file = "my_fav_recipes.txt"
        with open(target_file, "w") as file:
            file.write(combined_text)

        return jsonify({"message": f"Text extracted and saved to {target_file}"}), 200

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500
