import requests
import os
from flask import current_app

def generate_video_from_image(image_path):
    api_token = current_app.config.get('HF_API_TOKEN')
    if not api_token:
        raise ValueError("Hugging Face API token not configured.")

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
    headers = {"Authorization": f"Bearer {api_token}"}

    try:
        with open(image_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Assuming the API returns the video data directly
        # For simplicity, we'll save it locally and return a path/URL
        video_filename = os.path.basename(image_path).split('.')[0] + ".mp4"
        video_output_path = os.path.join(current_app.root_path, 'videos', video_filename)
        
        with open(video_output_path, "wb") as f:
            f.write(response.content)
            
        # Return a URL that the frontend can use to access the video
        # This assumes the 'videos' folder is served statically
        return f"/videos/{video_filename}"

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Hugging Face API request failed: {e}")
        raise Exception(f"Failed to generate video from Hugging Face API: {e}")
    except Exception as e:
        current_app.logger.error(f"Error in generate_video_from_image: {e}")
        raise Exception(f"An unexpected error occurred during video generation: {e}")
