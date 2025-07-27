def segment_into_sections(doc, filename):
    """Heuristically segments a PDF document, safely skipping image-only blocks."""
    sections = []
    current_section = None

    font_sizes = [
        span['size']
        for page in doc
        for block in page.get_text("dict").get("blocks", [])
        if block.get("type") == 0  # Process only text blocks
        for line in block.get("lines", [])
        for span in line.get("spans", [])
    ]
    if not font_sizes:
        return []

    median_size = sorted(font_sizes)[len(font_sizes) // 2]
    heading_threshold = median_size + 1.5

    for page_num, page in enumerate(doc):
        # Sort blocks by their vertical position
        blocks = sorted(page.get_text("dict").get("blocks", []), key=lambda b: b['bbox'][1])
        for block in blocks:
            # --- DEFENSIVE CHECK ---
            # Skip block if it's not a text block or has no lines
            if block.get("type") != 0 or not block.get("lines"):
                continue

            first_span = block["lines"][0]["spans"][0]
            text = " ".join([l['spans'][0]['text'] for l in block['lines']]).strip().replace("\n", " ")

            if first_span["size"] > heading_threshold and len(text.split()) < 20:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "document": filename, "section_title": text, "body_text": "",
                    "page_number": page_num + 1,
                }
            elif current_section:
                current_section["body_text"] += text + " "

    if current_section:
        sections.append(current_section)
    return [s for s in sections if s.get('body_text', '').strip()]