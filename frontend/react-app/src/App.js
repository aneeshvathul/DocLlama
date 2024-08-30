import React from 'react';
import FileUploader from './FileUploader';
import Prompt from './Prompt';

const App = () => {
  return (
    <div className = "App">
        <div>
          <h1>Welcome to DocLlama!</h1>
          <FileUploader />
          <Prompt />
        </div>
    </div>
  );
};

export default App;

