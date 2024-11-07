import React, { useState } from 'react';
import axios from 'axios';

function Upload() {
    const [file, setFile] = useState(null);
    const [transcription, setTranscription] = useState('');

    // Log the backend URL to verify it's loaded correctly
    console.log("Backend URL:", process.env.REACT_APP_BACKEND_URL);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL}/transcribe`, 
                formData, 
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            setTranscription(response.data.transcription);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div>
            <h1>Upload Audio for Transcription</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload and Transcribe</button>
            {transcription && <p>Transcription: {transcription}</p>}
        </div>
    );
}

export default Upload;
