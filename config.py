import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_development'
    HF_API_TOKEN = os.environ.get('HF_API_TOKEN')
    # Add other configurations here as needed
