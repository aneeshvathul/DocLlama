import faiss
import torch
import re

class VectorDatabase:
    def __init__(self, model, tokenizer):
        """
        Initialize the VectorDatabase with a model and FAISS index.
        
        :param model: Embeddings model from Hugging Face.
        :param tokenizer: Embeddings tokenizer from Hugging Face.
        """
        self.model = model
        self.tokenizer = tokenizer
        
        # Dimension of the embeddings produced by the model
        self.embedding_dim = self.model.config.hidden_size
        
        # FAISS index (using L2 distance metric by default)
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Store the text associated with each PDF
        self.pdfs = []

        # Store the text associated with the embeddings
        self.text_data = []


    def embed_text(self, text):
        """
        Generate embeddings for the given text using the model.
        
        :param text: List of text strings to embed.
        :return: Embeddings as numpy arrays.
        """
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state[:, 0, :]  # CLS token embeddings
        return embeddings.cpu().numpy()

    def add_pdf(self, pdf_text):
        """
        Add text data to the vector database.
        
        :param pdf_text: Raw pdf text to add.
        """
        sentences = re.split(r'(?<=[.!?]) +', pdf_text)
        self.pdfs.append(sentences)

    def search(self, query, k):
        """
        Search for the most similar texts to the query.
        
        :param query: Query text string.
        :param k: Number of top results to return.
        :return: List of top k most similar texts.
        """
        query_embedding = self.embed_text([query])
        distances, indices = self.index.search(query_embedding, k)
        results = [(self.text_data[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
        return results

    def remove_pdf(self, idx):
        """
        Remove a specific text from the vector database.
        
        :param idx: PDF index to remove.
        """
        self.pdfs.pop(idx)

    def enable_searching(self):
        """
        Prep the database to handle searches by setting FAISS indices
        """
        self.index.reset()
        self.text_data.clear()
        for parsed_pdf in self.pdfs:
            embeddings = self.embed_text(parsed_pdf)
            self.index.add(embeddings)
            self.text_data.extend(parsed_pdf)


