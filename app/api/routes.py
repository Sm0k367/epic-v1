from flask import request, jsonify, current_app
from app.api import bp
from app.services.hf_inference import generate_video_from_image
import os
import uuid

@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected image"}), 400
    
    if image:
        # Ensure the videos directory exists
        upload_folder = os.path.join(current_app.root_path, 'videos')
        os.makedirs(upload_folder, exist_ok=True)

        # Generate a unique filename for the uploaded image
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
        image_path = os.path.join(upload_folder, unique_filename)
        image.save(image_path)
        
        return jsonify({"message": "Image uploaded successfully", "image_path": unique_filename}), 200
    
    return jsonify({"error": "Something went wrong during upload"}), 500

@bp.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.get_json()
    image_filename = data.get('image_path')

    if not image_filename:
        return jsonify({"error": "No image path provided"}), 400

    image_path = os.path.join(current_app.root_path, 'videos', image_filename)

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    try:
        # Call the Hugging Face inference service
        video_url = generate_video_from_image(image_path)
        return jsonify({"message": "Video generation initiated", "video_url": video_url}), 200
    except Exception as e:
        current_app.logger.error(f"Error generating video: {e}")
        return jsonify({"error": str(e)}), 500
