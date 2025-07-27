from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
import sys

def download_all_models(save_path):
    os.makedirs(save_path, exist_ok=True)
    
    embedding_model_name = 'all-MiniLM-L6-v2'
    summarizer_model_name = 't5-small'
    
    print(f"Downloading {embedding_model_name} to {save_path}...")
    embedding_model = SentenceTransformer(embedding_model_name)
    embedding_model.save(os.path.join(save_path, embedding_model_name))
    print(f"Saved {embedding_model_name}.")
    
    print(f"\nDownloading {summarizer_model_name} to {save_path}...")
    summarizer_tokenizer = T5Tokenizer.from_pretrained(summarizer_model_name)
    summarizer_model = T5ForConditionalGeneration.from_pretrained(summarizer_model_name)
    
    model_path = os.path.join(save_path, summarizer_model_name)
    summarizer_tokenizer.save_pretrained(model_path)
    summarizer_model.save_pretrained(model_path)
    print(f"Saved {summarizer_model_name}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_save = sys.argv[1]
    else:
        path_to_save = "models"
    
    download_all_models(path_to_save)
