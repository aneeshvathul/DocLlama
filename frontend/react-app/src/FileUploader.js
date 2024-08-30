import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css'

const FileUploader = () => {
    const [files, setFiles] = useState([]);
    const [errors, setErrors] = useState([]);
    const [isUploading, setIsUploading] = useState(false); // Track upload status
    const fileInputRef = useRef(null); // Ref for the file input element

    const onFileChange = (event) => {
        setFiles(prevFiles => [...prevFiles, ...Array.from(event.target.files)]);
        setErrors([]);
    };

    const onFileUpload = () => {
        if (files.length === 0) {
            setErrors(['Please select at least one file']);
            return;
        }

        setIsUploading(true); // Set uploading state to true

        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
        });

        axios.post('http://127.0.0.1:5000/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log(response.data.message);
            setFiles([]); // Clear files after successful upload
            resetFileInput(); // Reset file input after successful upload
            setIsUploading(false); // Set uploading state to false
        })
        .catch(error => {
            setErrors(['Error uploading files']);
            console.error(error);
            setIsUploading(false); // Set uploading state to false even on error
        });
    };

    const removeFile = (fileName) => {
        const updatedFiles = files.filter(file => file.name !== fileName);
        setFiles(updatedFiles);
    };

    const resetFileInput = () => {
        if (fileInputRef.current) {
            fileInputRef.current.value = ''; // Reset the file input value
        }
    };

    return (
        <div>
            <div className = "center">
                <input
                    type="file"
                    accept=".pdf"
                    multiple
                    onChange={onFileChange}
                    ref={fileInputRef} // Attach ref to the input element
                />
                <button onClick={onFileUpload} disabled={isUploading}> {/* Disable button while uploading */}
                    Upload
                </button>
            </div>
            {/* Show the loading message when uploading */}
            {isUploading && (
                <div>
                    <p className = "center">Files uploading...</p>
                </div>
            )}

            {/* Show the list of selected files with a remove button */}
            {files.length > 0 && !isUploading && (
                <div>
                    <ul>
                        {files.map((file, index) => (
                            <li key={index} className = "center">
                                {'•  ' + file.name}
                                <button className = 'justify-button' onClick={() => removeFile(file.name)}>Remove</button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {errors.length > 0 && (
                <div style={{ color: 'red' }} className = "center">
                    {errors.map((error, index) => (
                        <p key={index}>{error}</p>
                    ))}
                </div>
            )}
        </div>
    );
};

export default FileUploader;
