document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const uploadButton = document.getElementById('uploadButton');
    const uploadStatus = document.getElementById('uploadStatus');
    const generateButton = document.getElementById('generateButton');
    const generationStatus = document.getElementById('generationStatus');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoMessage = document.getElementById('videoMessage');

    let uploadedImagePath = null; // To store the path of the uploaded image on the server

    // Enable/disable generate button based on image selection
    imageUpload.addEventListener('change', () => {
        if (imageUpload.files.length > 0) {
            uploadButton.disabled = false;
            uploadStatus.textContent = `Selected: ${imageUpload.files[0].name}`;
            uploadStatus.style.color = '#00ff00'; // Green for selected
            generateButton.disabled = true; // Disable generate until uploaded
            videoPlayer.style.display = 'none';
            videoMessage.textContent = '';
        } else {
            uploadButton.disabled = true;
            uploadStatus.textContent = 'No image selected.';
            uploadStatus.style.color = '#a0a0a0';
            generateButton.disabled = true;
        }
    });

    // Handle image upload
    uploadButton.addEventListener('click', async () => {
        const file = imageUpload.files[0];
        if (!file) {
            uploadStatus.textContent = 'Please select an image to upload.';
            uploadStatus.style.color = '#ff0000'; // Red for error
            return;
        }

        uploadStatus.textContent = 'Uploading image...';
        uploadStatus.style.color = '#00ffff'; // Cyan for processing

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                uploadedImagePath = data.image_path;
                uploadStatus.textContent = 'Image uploaded successfully!';
                uploadStatus.style.color = '#00ff00';
                generateButton.disabled = false; // Enable generate button
                generationStatus.textContent = 'Click "Generate Video" to create your masterpiece.';
                generationStatus.style.color = '#a0a0a0';
            } else {
                uploadStatus.textContent = `Upload failed: ${data.error || 'Unknown error'}`;
                uploadStatus.style.color = '#ff0000';
                generateButton.disabled = true;
            }
        } catch (error) {
            console.error('Error during image upload:', error);
            uploadStatus.textContent = 'Network error during upload. Please try again.';
            uploadStatus.style.color = '#ff0000';
            generateButton.disabled = true;
        }
    });

    // Handle video generation
    generateButton.addEventListener('click', async () => {
        if (!uploadedImagePath) {
            generationStatus.textContent = 'Please upload an image first.';
            generationStatus.style.color = '#ff0000';
            return;
        }

        generateButton.disabled = true;
        generationStatus.textContent = 'Generating video... This may take a moment.';
        generationStatus.style.color = '#ff00ff'; // Magenta for processing
        videoPlayer.style.display = 'none';
        videoMessage.textContent = '';

        try {
            const response = await fetch('/api/generate-video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_path: uploadedImagePath })
            });

            const data = await response.json();

            if (response.ok) {
                generationStatus.textContent = 'Video generated successfully!';
                generationStatus.style.color = '#00ff00';
                videoPlayer.src = data.video_url;
                videoPlayer.style.display = 'block';
                videoPlayer.load(); // Load the new video
                videoPlayer.play(); // Autoplay the video
                videoMessage.textContent = 'Enjoy your AI-generated video!';
                videoMessage.style.color = '#00ff00';
            } else {
                generationStatus.textContent = `Generation failed: ${data.error || 'Unknown error'}`;
                generationStatus.style.color = '#ff0000';
                videoPlayer.style.display = 'none';
                videoMessage.textContent = '';
            }
        } catch (error) {
            console.error('Error during video generation:', error);
            generationStatus.textContent = 'Network error during video generation. Please try again.';
            generationStatus.style.color = '#ff0000';
            videoPlayer.style.display = 'none';
            videoMessage.textContent = '';
        } finally {
            generateButton.disabled = false; // Re-enable button after attempt
        }
    });
});
