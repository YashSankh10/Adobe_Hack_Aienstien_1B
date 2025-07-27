from transformers import T5ForConditionalGeneration, T5Tokenizer
from loguru import logger

def generate_summaries(top_sections, model, tokenizer):
    """Generates a concise summary for each of the top-ranked sections."""
    if model is None or tokenizer is None:
        logger.warning("Summarizer model not loaded. Skipping summary generation.")
        return []

    summaries = []
    for section in top_sections:
        input_text = f"summarize: {section['section_title']}. {section['body_text']}"
        inputs = tokenizer.encode(
            input_text, return_tensors="pt", max_length=512, truncation=True
        )
        summary_ids = model.generate(
            inputs, max_length=120, min_length=40, num_beams=4, early_stopping=True
        )
        refined_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        summaries.append({
            "document": section["document"],
            "refined_text": refined_text,
            "page_number": section["page_number"],
        })
        
    return summaries