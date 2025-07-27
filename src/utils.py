import os
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

# This absolute path points to the models inside the Docker image
MODEL_DIR = "/pipeline_models"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
SUMMARIZER_MODEL_NAME = "t5-small"

def load_models():
    """Loads all models from the absolute path inside the container."""
    embed_path = os.path.join(MODEL_DIR, EMBEDDING_MODEL_NAME)
    embedding_model = SentenceTransformer(embed_path)
    
    summarizer_path = os.path.join(MODEL_DIR, SUMMARIZER_MODEL_NAME)
    summarizer_model = T5ForConditionalGeneration.from_pretrained(summarizer_path)
    summarizer_tokenizer = T5Tokenizer.from_pretrained(summarizer_path)
    
    return embedding_model, summarizer_model, summarizer_tokenizer