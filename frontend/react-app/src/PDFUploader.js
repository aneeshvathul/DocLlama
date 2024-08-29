import React, { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`;

const PDFUploader = ({ setExtractedTexts }) => {
    const [pdfFiles, setPdfFiles] = useState([]);

    const onFileChange = async (event) => {
        const files = Array.from(event.target.files);
        const newPdfFiles = [...pdfFiles, ...files];
        setPdfFiles(newPdfFiles);

        await extractAndSetTexts(newPdfFiles);
    };

    const extractTextFromPDF = async (file) => {
        const fileReader = new FileReader();
        return new Promise((resolve) => {
            fileReader.onload = async function () {
                const typedArray = new Uint8Array(this.result);

                const pdf = await pdfjsLib.getDocument(typedArray).promise;
                let extractedText = '';

                for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
                    const page = await pdf.getPage(pageNumber);
                    const textContent = await page.getTextContent();
                    const pageText = textContent.items.map(item => item.str).join(' ');
                    extractedText += pageText + '\n';
                }

                resolve(extractedText);
            };
            fileReader.readAsArrayBuffer(file);
        });
    };

    const extractAndSetTexts = async (files) => {
        const extractedTexts = await Promise.all(files.map(file => extractTextFromPDF(file)));
        setExtractedTexts(extractedTexts);
    };

    const removePdf = async (index) => {
        const newPdfFiles = [...pdfFiles];
        newPdfFiles.splice(index, 1);
        setPdfFiles(newPdfFiles);

        // Re-extract text after removal
        await extractAndSetTexts(newPdfFiles);
    };

    return (
        <div>
            <input type="file" accept="application/pdf" onChange={onFileChange} multiple />
            <ul>
                {pdfFiles.map((file, index) => (
                    <li key={index}>
                        {file.name}
                        <button onClick={() => removePdf(index)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PDFUploader;