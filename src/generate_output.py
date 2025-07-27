import json
from datetime import datetime, timezone

def create_final_json(output_path, doc_filenames, persona, job_to_be_done, ranked_sections, summaries):
    """Formats the data and saves it to the specified output JSON file."""
    output_data = {
        "metadata": {
            "input_documents": doc_filenames,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        "extracted_sections": [
            {
                "document": s["document"],
                "section_title": s["section_title"],
                "importance_rank": s["importance_rank"],
                "page_number": s["page_number"]
            } for s in ranked_sections
        ],
        "subsection_analysis": summaries
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)