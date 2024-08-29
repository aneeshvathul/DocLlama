from mlx_lm import load, generate
from transformers import AutoModel, AutoTokenizer
from vector_database import VectorDatabase

# def set_vector_database(long_text):
#     """
#     Create a vector database instance parsed by sentences
#     """
#     global current_vdb
#     sentences = re.split(r'(?<=[.!?]) +', long_text)
#     vdb = VectorDatabase(embeddings_model, embeddings_tokenizer)
#     vdb.add_texts(sentences)
#     current_vdb = vdb
    
def load_models():
    """
    Load in an 8-bit-quantized instance of Llama-3-8B
    """
    global llama_model, llama_tokenizer, embeddings_model, embeddings_tokenizer
    llama_model, llama_tokenizer = load("mlx-community/Meta-Llama-3-8B-Instruct-8bit")
    embeddings_model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    embeddings_tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    
def run_inference(prompt):
    """
    Run query prompt inference in a user-and-assistant context
    """
    begin_token = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>"
    end_token = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    query_prompt = f"{begin_token}{prompt}{end_token}"
    response = generate(
        model = llama_model, 
        tokenizer = llama_tokenizer, 
        prompt = query_prompt,
        max_tokens = 500,
        verbose = True)

if __name__ == "__main__":
    global vdb
    load_models()
    vdb = VectorDatabase(embeddings_model, embeddings_tokenizer)

