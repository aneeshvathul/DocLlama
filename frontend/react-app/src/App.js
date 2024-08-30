import React from 'react';
import FileUploader from './FileUploader';
import Prompt from './Prompt';
import './App.css'

const App = () => {
  return (
    <div>
        <h1 className = "center">Welcome to DocLlama!</h1>
        <FileUploader />
        <Prompt />
    </div>
  );
};

export default App;

