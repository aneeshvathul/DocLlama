import React, { useState } from 'react';
import PDFUploader from './PDFUploader';

const App = () => {
    const [extractedTexts, setExtractedTexts] = useState([]);

    return (
        <div className="App">
            <h1>Multi-PDF Text Extractor</h1>
            <PDFUploader setExtractedTexts={setExtractedTexts} />
            {console.log(extractedTexts)}
        </div>
    );
};

export default App;
