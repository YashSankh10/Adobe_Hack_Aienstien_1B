import json
import time
import os
import sys
from datetime import datetime, timezone
from loguru import logger

from src.extract_text import process_all_pdfs
from src.embed_and_rank import rank_sections_by_relevance
from src.summarize import generate_summaries
from src.generate_output import create_final_json
from src.utils import load_models

def main(input_json_path, docs_folder_path):
    start_time = time.time()
    logger.info("Starting Persona-Driven Document Intelligence Pipeline...")

    with open(input_json_path, 'r') as f:
        inputs = json.load(f)

    persona = inputs["persona"]["role"]
    job_to_be_done = inputs["job_to_be_done"]["task"]
    doc_filenames = [doc['filename'] for doc in inputs["documents"]]
    
    logger.info(f"Persona: {persona}")
    logger.info(f"Task: {job_to_be_done}")

    logger.info("Loading embedding and summarization models...")
    embedding_model, summarizer_model, summarizer_tokenizer = load_models()

    logger.info(f"Processing {len(doc_filenames)} PDF documents...")
    all_sections = process_all_pdfs(docs_folder_path, doc_filenames)

    if not all_sections:
        logger.error("No sections could be extracted. Exiting.")
        return

    query = f"Role: {persona}. Task: {job_to_be_done}"
    logger.info("Embedding and ranking sections by relevance...")
    ranked_sections = rank_sections_by_relevance(query, all_sections, embedding_model)

    top_sections = ranked_sections[:5]

    logger.info(f"Generating summaries for the top {len(top_sections)} sections...")
    summaries = generate_summaries(top_sections, summarizer_model, summarizer_tokenizer)
    
    # Define the output path and call the file-writing function
    output_json_path = "challenge1b_output.json"
    logger.info(f"Assembling final output JSON to {output_json_path}...")
    create_final_json(
        output_path=output_json_path,
        doc_filenames=doc_filenames,
        persona=persona,
        job_to_be_done=job_to_be_done,
        ranked_sections=top_sections,
        summaries=summaries
    )

    end_time = time.time()
    logger.info(f"Pipeline finished in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <path_to_input_json> <path_to_docs_folder>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
