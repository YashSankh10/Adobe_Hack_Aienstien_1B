from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

def load_models(model_dir, embedding_model_name, summarizer_model_name):
    """Loads all models from a local directory."""
    # Embedding model is loaded here for consistency, though only used in this module.
    embed_path = os.path.join(model_dir, embedding_model_name)
    embedding_model = SentenceTransformer(embed_path)
    
    # Summarizer is loaded separately in its module but could be done here.
    # We return None for summarizer parts as they are handled in summarize.py
    return embedding_model, None, None # Simplified for this module

def rank_sections_by_relevance(query, sections, model):
    """Encodes query and sections, then ranks sections by cosine similarity."""
    if not sections:
        return []
        
    query_embedding = model.encode([query])
    
    section_texts = [f"{s['section_title']}\n{s['body_text']}" for s in sections]
    section_embeddings = model.encode(section_texts, show_progress_bar=False)
    
    similarities = cosine_similarity(query_embedding, section_embeddings)[0]
    
    # Add similarity score to each section and sort
    for i, section in enumerate(sections):
        section['relevance_score'] = similarities[i]
        
    sorted_sections = sorted(sections, key=lambda x: x['relevance_score'], reverse=True)
    
    # Assign rank and format for output
    final_ranked_list = []
    for rank, section in enumerate(sorted_sections):
        final_ranked_list.append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": rank + 1,
            "page_number": section["page_number"],
            # Keep body_text for summarization step, remove before final output
            "body_text": section["body_text"]
        })
        
    return final_ranked_list