import React, { useState } from 'react'; // Ensure React and useState are imported
import axios from 'axios'; // Ensure axios is imported

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [detections, setDetections] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const validateFile = (file) => {
        // File type validation
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            throw new Error('Invalid file type. Please upload a JPEG, PNG, or GIF image.');
        }
        // File size validation (e.g., 5MB limit)
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

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post('http://localhost:5000/detect', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 30000, // Timeout of 30 seconds
                maxContentLength: 5 * 1024 * 1024, // Max content length of 5MB
            });
            setDetections(response.data);
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
                {isLoading ? 'Uploading...' : 'Detect'}
            </button>
            
            {error && <div className="error-message">{error}</div>}
            
            {detections.length > 0 && (
                <div className="detections-container">
                    <h3>Detections:</h3>
                    <ul>
                        {detections.map((detection, index) => (
                            <li key={index}>
                                Class: {detection.class}, 
                                Confidence: {(detection.confidence * 100).toFixed(2)}%
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ImageUpload; // Ensure the component is exported
