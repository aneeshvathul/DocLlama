import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

const Prompt = () => {
    const [prompt, setPrompt] = useState('');
    const [modelResponse, setModelResponse] = useState('')

    const handleSubmit = () => {
        console.log('Prompt submitted:', prompt);
        setModelResponse('Loading...');
        
        axios.post('http://127.0.0.1:5000/run-inference', { prompt: prompt }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            setModelResponse(response.data.modelResponse);
            console.log("Query successful!");
        })
        .catch(error => {
            setModelResponse("Error generating response");
            console.error(error);
        });
    };

    return (
        <div> 
            <div className = 'center'>
                <textarea
                    value={prompt}
                    onChange={
                        (e) => {
                        setPrompt(e.target.value);
                        if (modelResponse)
                            setModelResponse('')
                        }
                    }
                    placeholder="Type your prompt here..."
                    rows="10"
                    cols="50"
                />
            </div>
            <br />
            <div className = 'center-associated-button'>
                <button onClick={handleSubmit}>Submit</button>
            </div>
            <div className = 'center'>
                <textarea
                    value={modelResponse}
                    onChange={
                        (e) => setModelResponse(e.target.value)
                    }
                    rows="10"
                    cols="50"
                />
            </div>
            <br />
        </div>
    );
};

export default Prompt;
