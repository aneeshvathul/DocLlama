from mlx_lm import load, generate
from transformers import AutoModel, AutoTokenizer
from vector_database import VectorDatabase
from flask import Flask, request, jsonify
import pdfplumber
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows all origins by default

# Initialize global variables
llama_model = None
llama_tokenizer = None
embeddings_model = None
embeddings_tokenizer = None
vdb = None
server_initialized = False

def load_models():
    """
    Load in an 8-bit-quantized instance of Llama-3-8B and embedding models.
    """
    global llama_model, llama_tokenizer, embeddings_model, embeddings_tokenizer
    if llama_model is None and llama_tokenizer is None:
        llama_model, llama_tokenizer = load("mlx-community/Meta-Llama-3-8B-Instruct-8bit")
    if embeddings_model is None and embeddings_tokenizer is None:
        embeddings_model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        embeddings_tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def initialize_server():
    global embeddings_model, embeddings_tokenizer, vdb, server_initialized
    if not server_initialized:
        load_models()
        vdb = VectorDatabase(embeddings_model, embeddings_tokenizer)
        server_initialized = True

@app.route('/run-inference', methods=['POST'])
def run_inference():
    """
    Run query prompt inference in a user-and-assistant context.
    """
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    if not vdb.pdfs:
        return jsonify({"error": "Documents is required"}), 400
    
    k = min(10, len(vdb.text_data))
    closest_sentences = vdb.search(prompt, k)
    context = " ".join([sentence for sentence, dist in closest_sentences])

    query_prompt = f"""<|begin_of_text|>
    <|start_header_id|>system<|end_header_id|>

        {context}<|eot_id|>

    <|start_header_id|>user<|end_header_id|>

        {prompt}<|eot_id|>

    <|start_header_id|>assistant<|end_header_id|>
    """

    try:
        response = generate(
            model=llama_model, 
            tokenizer=llama_tokenizer, 
            prompt=query_prompt,
            max_tokens=300,
            verbose=True
        )
        if not response.strip():
            return jsonify({"modelResponse": "Sorry, I don't have enough information on that."})
        return jsonify({"modelResponse": response})
    except Exception as e:
        return jsonify({"error": f"Query unsuccessful: {str(e)}"}), 400

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

@app.route('/upload', methods=['POST'])
def upload_files():
    if not vdb:
        return jsonify({"error": "Server not initialized"}), 400

    vdb.reset()
    
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected"}), 400

    errors = []

    for file in files:
        if file.filename.endswith('.pdf'):
            try:
                if file.filename not in vdb.file_names:
                    text = extract_text_from_pdf(file)
                    vdb.add_pdf(text, file.filename)
            except Exception as e:
                errors.append(f"Error processing file {file.filename}: {str(e)}")
        else:
            errors.append(f"Invalid file type: {file.filename}")

    if errors:
        return jsonify({"errors": errors}), 400
    
    vdb.enable_searching()
    return jsonify({"message": "Files uploaded"}), 200

if __name__ == "__main__":
    initialize_server()
    app.run(debug=False)
