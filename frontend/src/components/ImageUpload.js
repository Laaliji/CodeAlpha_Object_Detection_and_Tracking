import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    // Update this line in ImageUpload.js
const [selectedFile, setSelectedFile] = useState(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
const [annotatedImageUrl, setAnnotatedImageUrl] = useState(null);

    const validateFile = (file) => {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            throw new Error('Invalid file type. Please upload a JPEG, PNG, or GIF image.');
        }
        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            throw new Error('File size too large. Please upload an image under 5MB.');
        }
    };

    const handleFileChange = (event) => {
        try {
            const file = event.target.files[0];
            if (file) {
                validateFile(file);
                setSelectedFile(file);
                setError(null);
            }
        } catch (err) {
            setError(err.message);
            setSelectedFile(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError("Please select an image first.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setAnnotatedImageUrl(null);

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post('http://localhost:5001/detect', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                responseType: 'blob',
            });

            const imageUrl = URL.createObjectURL(response.data);
            setAnnotatedImageUrl(imageUrl); // Display the detected image

        } catch (error) {
            setError(error.response?.data?.message || "Error uploading image. Please try again.");
            console.error("Upload error:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload an Image for Detection</h2>
            <input 
                type="file" 
                accept="image/*"
                onChange={handleFileChange}
                disabled={isLoading} 
            />
            <button 
                onClick={handleUpload}
                disabled={!selectedFile || isLoading}
            >
                {isLoading ? 'Processing...' : 'Detect'}
            </button>
            
            {error && <div className="error-message">{error}</div>}
            
            {annotatedImageUrl && (
                <div className="download-container">
                    <a href={annotatedImageUrl} download="detected_image.png">
                        <button>Download Detected Image</button>
                    </a>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
