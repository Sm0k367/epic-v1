from flask import render_template, current_app, send_from_directory
from app.main import bp
import os

@bp.route('/')
@bp.route('/index')
def index():
    return send_from_directory(current_app.static_folder, 'index.html')

# Route to serve static files directly from the static folder
@bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(current_app.static_folder, filename)

# Route to serve generated video files from the videos folder
@bp.route('/videos/<path:filename>')
def serve_video(filename):
    videos_folder = os.path.join(current_app.root_path, 'videos')
    return send_from_directory(videos_folder, filename)
